"""Tryton / GNU Health JSON-RPC and Proteus client."""

from __future__ import annotations

import logging
import os
from typing import Any

import requests

logger = logging.getLogger(__name__)

PROTEUS_AVAILABLE = False
try:
    from proteus import Model, config as proteus_config

    PROTEUS_AVAILABLE = True
except ImportError:
    proteus_config = None  # type: ignore
    Model = None  # type: ignore


class TrytonError(Exception):
    """Raised when Tryton RPC returns an error."""


class TrytonClient:
    """JSON-RPC client for Tryton 7 / GNU Health 5."""

    AUTH_METHODS = (
        ("common.authenticate", lambda db, u, p, lang: [db, u, {"password": p}, lang]),
        ("common.login", lambda db, u, p, lang: [db, u, p]),
        ("common.db.login", lambda db, u, p, lang: [db, u, p]),
    )

    def __init__(
        self,
        url: str,
        database: str,
        username: str,
        password: str,
        language: str = "en",
    ) -> None:
        base = url.rstrip("/")
        self.database = database
        self.username = username
        self.password = password
        self.language = language
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.rpc_url = f"{base}/{database}/"
        self.uid: int | None = None
        self._request_id = 0
        self._use_proteus = False

    def connect(self) -> int:
        """Authenticate via Proteus (if available) or JSON-RPC."""
        if PROTEUS_AVAILABLE:
            try:
                return self._connect_proteus()
            except Exception as exc:
                logger.debug("Proteus connect failed, falling back to JSON-RPC: %s", exc)

        last_error: Exception | None = None
        for method, param_fn in self.AUTH_METHODS:
            try:
                params = param_fn(
                    self.database, self.username, self.password, self.language
                )
                result = self._rpc(method, params, auth_attempt=True)
                if result:
                    self.uid = int(result[0] if isinstance(result, list) else result)
                    logger.info(
                        "Connected via %s as user id %s", method, self.uid
                    )
                    return self.uid
            except TrytonError as exc:
                last_error = exc
                logger.debug("%s failed: %s", method, exc)

        raise TrytonError(
            f"Authentication failed for '{self.username}' on '{self.database}': {last_error}"
        )

    def _connect_proteus(self) -> int:
        assert proteus_config is not None

        config_file = os.environ.get(
            "GNUHEALTH_TRYTOND_CONF",
            "/opt/gnuhealth/his-50/etc/trytond.conf",
        )
        if os.path.isfile(config_file):
            proteus_config.set_trytond(
                database=self.database,
                user=self.username,
                config_file=config_file,
            )
            self._use_proteus = True
            User = Model.get("res.user")
            uid = User.find([("login", "=", self.username)])[0].id
            self.uid = uid
            logger.info("Connected via Proteus/trytond as user id %s", self.uid)
            return uid

        base_url = self.rpc_url.rsplit(f"/{self.database}/", 1)[0] + "/"
        with proteus_config.set_xmlrpc_session(
            base_url,
            self.username,
            password=self.password,
        ):
            self._use_proteus = True
            User = Model.get("res.user")
            uid = User.find([("login", "=", self.username)])[0].id
            self.uid = uid
            logger.info("Connected via Proteus/xmlrpc as user id %s", self.uid)
            return uid

    def _rpc(
        self,
        method: str,
        params: list[Any] | None = None,
        auth_attempt: bool = False,
    ) -> Any:
        self._request_id += 1
        payloads = [
            {"jsonrpc": "2.0", "method": method, "params": params or [], "id": self._request_id},
            {"method": method, "params": params or []},
        ]
        last_error: str | None = None
        for payload in payloads:
            response = self.session.post(self.rpc_url, json=payload, timeout=120)
            if response.status_code == 401 and not auth_attempt:
                raise TrytonError("Session expired or unauthorized (401)")
            if response.status_code >= 400:
                last_error = f"HTTP {response.status_code}: {response.text[:300]}"
                continue
            try:
                data = response.json()
            except ValueError:
                last_error = f"Non-JSON response: {response.text[:300]}"
                continue
            if "error" in data:
                err = data["error"]
                last_error = str(err)
                continue
            return data.get("result")
        raise TrytonError(f"RPC {method} failed: {last_error}")

    def call(self, model: str, method: str, *args: Any) -> Any:
        if self.uid is None:
            raise TrytonError("Not connected — call connect() first")
        if self._use_proteus and PROTEUS_AVAILABLE:
            return self._call_proteus(model, method, *args)
        return self._rpc(f"model.{model}.{method}", list(args))

    def _call_proteus(self, model: str, method: str, *args: Any) -> Any:
        assert Model is not None
        try:
            cls = Model.get(model)
        except KeyError as exc:
            raise TrytonError(f"Model not found: {model}") from exc
        if method == "search":
            domain, offset, limit, order, context = (
                list(args) + [None, None, {}]
            )[:5]
            records = cls.find(domain or [], offset=offset or 0, limit=limit)
            return [r.id for r in records]
        if method == "search_count":
            return len(cls.find(args[0] if args else []))
        if method == "read":
            ids, fields = args[0], args[1] if len(args) > 1 else []
            return [
                {f: getattr(cls(id), f) for f in fields} if fields
                else {"id": id}
                for id in ids
            ]
        if method == "create":
            values_list = args[0]
            if isinstance(values_list, dict):
                values_list = [values_list]
            context = args[1] if len(args) > 1 else {}
            result = cls._proxy.create(values_list, context or {})
            return result if len(result) > 1 else result[0]
        if method == "write":
            ids, vals = args[0], args[1]
            context = args[2] if len(args) > 2 else {}
            cls._proxy.write(ids, vals, context or {})
            return True
        raise TrytonError(f"Proteus method not implemented: {model}.{method}")

    def search(
        self,
        model: str,
        domain: list | None = None,
        offset: int = 0,
        limit: int | None = None,
        order: list | None = None,
        context: dict | None = None,
    ) -> list[int]:
        return self.call(
            model, "search", domain or [], offset, limit, order, context or {}
        )

    def search_count(self, model: str, domain: list | None = None) -> int:
        return self.call(model, "search_count", domain or [], {})

    def read(
        self, model: str, ids: list[int], fields: list[str] | None = None
    ) -> list[dict]:
        if not ids:
            return []
        return self.call(model, "read", ids, fields or [])

    def create(self, model: str, values: list[dict] | dict) -> list[int] | int:
        if isinstance(values, dict):
            values = [values]
        return self.call(model, "create", values, {})

    def write(self, model: str, ids: list[int], values: dict) -> bool:
        return self.call(model, "write", ids, values, {})

    def delete(self, model: str, ids: list[int]) -> bool:
        return self.call(model, "delete", ids, {})

    def model_exists(self, model: str) -> bool:
        try:
            self.search(model, [], limit=1)
            return True
        except (TrytonError, KeyError):
            return False

    def find_one(self, model: str, domain: list) -> dict | None:
        ids = self.search(model, domain, limit=1)
        if not ids:
            return None
        rows = self.read(model, ids)
        return rows[0] if rows else None

    def find_or_create(
        self,
        model: str,
        domain: list,
        values: dict,
        idempotent: bool = True,
    ) -> tuple[int, bool]:
        if idempotent:
            existing = self.search(model, domain, limit=1)
            if existing:
                return existing[0], False
        new_id = self.create(model, values)
        if isinstance(new_id, list):
            return new_id[0], True
        return new_id, True

    def batch_create(
        self,
        model: str,
        records: list[dict],
        batch_size: int = 100,
        label: str = "records",
    ) -> list[int]:
        all_ids: list[int] = []
        total = len(records)
        for start in range(0, total, batch_size):
            batch = records[start : start + batch_size]
            for vals in batch:
                new_id = self.create(model, vals)
                if isinstance(new_id, list):
                    all_ids.extend(new_id)
                else:
                    all_ids.append(new_id)
            done = min(start + batch_size, total)
            logger.info("Created %s/%s %s on %s", done, total, label, model)
        return all_ids
