/**
 * IST HIS optional tweaks for GNU Health SAO.
 * Deploy to SAO web root as custom.js (auto-loaded by SAO after tryton-sao.js).
 * Keep minimal — do not break wizards or JSON-RPC.
 *
 * Session handoff (same-origin):
 *   React stores ist-health-session { uid, username, database, sessionToken }.
 *   SAO restores from sao_session_{db} { login, user_id, session }.
 *   This file copies IST → SAO before Sao.login() on DOMContentLoaded, and
 *   ensures #database is in the hash so get_credentials skips the login dialog.
 *
 * Icon colors:
 * - Tryton monochrome SVGs inherit fill from Sao.config.icon_colors[0] via
 *   ICONFACTORY._convert (default teal #267f82).
 * - GNU Health module icons are multi-color SVGs with hardcoded teal/cyan
 *   fills/gradients (#08828B, #028189, #34A6AE, …) AND beige/peach “skin”
 *   fills (e.g. Party heads). Setting only the root <svg fill> does NOT
 *   recolor those. We patch _convert to rewrite teal + beige hexes to IST
 *   navy, then walk menu <img> blobs as a safety net (MutationObserver).
 */
(function () {
  'use strict';

  var IST_SESSION_KEY = 'ist-health-session';

  /**
   * Bridge React Tryton session into SAO localStorage before Sao.login runs.
   * Must run at parse time (before document.ready handlers from tryton-sao.js).
   */
  function handoffIstSessionToSao() {
    try {
      var raw = localStorage.getItem(IST_SESSION_KEY);
      if (!raw) return null;
      var ist = JSON.parse(raw);
      if (!ist || !ist.database || !ist.username || !ist.sessionToken || !ist.uid) {
        return null;
      }
      var key = 'sao_session_' + ist.database;
      localStorage.setItem(
        key,
        JSON.stringify({
          login: ist.username,
          user_id: ist.uid,
          session: ist.sessionToken,
        })
      );
      // Sao.Session.get_credentials only restores when hash has the database name.
      var hashDb = (window.location.hash || '')
        .replace(/^(#(!|))/, '')
        .split('/', 1)[0];
      if (!hashDb) {
        window.location.hash = ist.database;
      }
      return ist;
    } catch (e) {
      return null;
    }
  }

  handoffIstSessionToSao();

  var IST_NAVY = '#0a1f44';
  var IST_MUTED = '#3d4f6a';
  var IST_GOLD = '#c9a66b';

  /** Explicit SAO / common GH teal accents (case-insensitive). */
  var TEAL_EXPLICIT_RE =
    /#(?:267f82|1abc9c|16a085|32ad52|28a745|20c997|17a2b8|08828b|028189|086973|046973|076a72|036973|016f72|007c84|007d86|01737a|0a8991|0c838c|118389|157880|17717a|17808a|1b8b93|1e8991|288f95|2a9ba1|2c9ba4|32a5ae|32a7af|33a8ae|33a9af|34a6ae|349fa6|35a9af|38929a|00afb3|00b0b5|00b2b6|01a7aa|01a9ac|27b4b7|2ab6b9|47abb0|4dbbbe|5bbac2|5fbec3|61b0b4|66a5ad|69b8bd|6ab9bd|6bb4b7|6fa6ad|78c6c9|7abbbe|81bbc1|93c6c9|97ced1|9ad1d4|9fd2d5|a1d5d9|a3d7da|b2d6d9|b7d7d9)\b/gi;

  function parseHex(hex) {
    var h = String(hex || '').replace('#', '');
    if (h.length === 3) {
      h = h[0] + h[0] + h[1] + h[1] + h[2] + h[2];
    }
    if (h.length !== 6 || /[^0-9a-f]/i.test(h)) {
      return null;
    }
    return {
      r: parseInt(h.slice(0, 2), 16),
      g: parseInt(h.slice(2, 4), 16),
      b: parseInt(h.slice(4, 6), 16),
    };
  }

  /**
   * Hue/sat/lightness for a hex. Returns null if unparsable.
   */
  function hexHsl(hex) {
    var rgb = parseHex(hex);
    if (!rgb) {
      return null;
    }
    var r = rgb.r / 255;
    var g = rgb.g / 255;
    var b = rgb.b / 255;
    var max = Math.max(r, g, b);
    var min = Math.min(r, g, b);
    var d = max - min;
    var lightness = (max + min) / 2;
    var hue = 0;
    if (d > 0) {
      if (max === r) {
        hue = ((g - b) / d + (g < b ? 6 : 0)) * 60;
      } else if (max === g) {
        hue = ((b - r) / d + 2) * 60;
      } else {
        hue = ((r - g) / d + 4) * 60;
      }
    }
    var sat =
      lightness === 1 || lightness === 0
        ? 0
        : d / (1 - Math.abs(2 * lightness - 1));
    return { hue: hue, sat: sat, lightness: lightness };
  }

  /**
   * True for saturated green / teal / cyan used by GNU Health icons.
   * Skips near-white pale tints and near-gray neutrals.
   */
  function isTealOrGreenHex(hex) {
    var hsl = hexHsl(hex);
    if (!hsl) {
      return false;
    }
    if (hsl.lightness > 0.78 || hsl.lightness < 0.08 || hsl.sat < 0.1) {
      return false;
    }
    return hsl.hue >= 140 && hsl.hue <= 200 && hsl.sat > 0.18;
  }

  /**
   * Beige / tan / peach “skin” fills on multi-color GH icons (e.g. Party heads).
   * These are not teal, so earlier passes left them — force navy monochrome.
   */
  function isBeigeOrFleshHex(hex) {
    if (
      /^#(?:e8d5b7|e6c9a8|d4c4a8|d2b48c|c8b89a|c9a66b|d4b87a|f0e6d4|f5d0b0|f5deb3|ffe4c4|ffdead|deb887|daa520|cd853f|d2b48c|e8c39e|e0c09a|f4e4c1|f7e7ce|f3e5ab|ead9c6|e5d3b3|dcc7a8|cbb994|b8a07a|a89070|c4a484|e6be8a|f0d9b5|f2e6d0|efe0c8|e9d5b5)$/i.test(
        hex
      )
    ) {
      return true;
    }
    var hsl = hexHsl(hex);
    if (!hsl) {
      return false;
    }
    // Warm beige / peach / tan heads (not saturated orange favorites)
    if (hsl.lightness < 0.42 || hsl.lightness > 0.94 || hsl.sat < 0.08) {
      return false;
    }
    if (hsl.hue >= 15 && hsl.hue <= 55 && hsl.sat <= 0.65) {
      return true;
    }
    // Desaturated warm gray-beige used as faces
    if (hsl.hue >= 20 && hsl.hue <= 50 && hsl.sat >= 0.05 && hsl.sat < 0.22 && hsl.lightness > 0.55) {
      return true;
    }
    return false;
  }

  function isNearNavyHex(hex) {
    return /^#(?:0a1f44|071428|1a3056|3d4f6a|0a1f44ff|001f3f|002147|0b1e3a|12253f)$/i.test(
      hex
    );
  }

  /**
   * @param {string} hex
   * @param {string} [fillColor] — when IST_GOLD (favorites), preserve gold accents
   */
  function shouldRecolorHex(hex, fillColor) {
    if (!hex) {
      return false;
    }
    if (/^#(fff|ffffff|000|000000)$/i.test(hex)) {
      return false;
    }
    if (isNearNavyHex(hex) && (!fillColor || fillColor === IST_NAVY)) {
      return false;
    }
    // Favorites / gold path: keep warm gold accents
    if (
      fillColor === IST_GOLD &&
      /^#(c9a66b|d4b87a|f0e6d4|f08701|f3a33b|f9b97a|fabf73|fbb579|fbd19e)$/i.test(hex)
    ) {
      return false;
    }
    // Navy monochrome path: do NOT keep beige/gold-muted — Party heads must go navy
    TEAL_EXPLICIT_RE.lastIndex = 0;
    if (TEAL_EXPLICIT_RE.test(hex)) {
      return true;
    }
    if (isTealOrGreenHex(hex)) {
      return true;
    }
    if (fillColor !== IST_GOLD && isBeigeOrFleshHex(hex)) {
      return true;
    }
    return false;
  }

  function svgNeedsIstRecolor(svgText, fillColor) {
    var hexes = svgText.match(/#[0-9a-fA-F]{3,8}/g) || [];
    for (var i = 0; i < hexes.length; i++) {
      if (shouldRecolorHex(hexes[i], fillColor)) {
        return true;
      }
    }
    return false;
  }

  /** @deprecated use svgNeedsIstRecolor — kept name for call-site clarity in walks */
  function svgHasTeal(svgText) {
    return svgNeedsIstRecolor(svgText, IST_NAVY);
  }

  function recolorSvgText(svgText, fillColor) {
    if (!svgText || typeof svgText !== 'string') {
      return svgText;
    }
    var color = fillColor || IST_NAVY;
    var out = svgText.replace(/#([0-9a-fA-F]{3,8})\b/g, function (match) {
      return shouldRecolorHex(match, color) ? color : match;
    });

    var open = out.match(/<svg\b[^>]*>/i);
    if (open) {
      var tag = open[0];
      if (/\bfill="/i.test(tag)) {
        tag = tag.replace(/\bfill="[^"]*"/i, 'fill="' + color + '"');
      } else {
        tag = tag.replace(/<svg\b/i, '<svg fill="' + color + '"');
      }
      out = out.replace(open[0], tag);
    }
    return out;
  }

  function convertSvgToBlobUrl(svgText, fillColor) {
    var colored = recolorSvgText(svgText, fillColor || IST_NAVY);
    return window.URL.createObjectURL(
      new Blob([colored], { type: 'image/svg+xml' })
    );
  }

  function patchIconFactory() {
    if (!Sao.common || !Sao.common.ICONFACTORY) {
      return;
    }
    var factory = Sao.common.ICONFACTORY;

    // Stronger _convert: root fill + rewrite hardcoded GH teals
    factory._convert = function (data) {
      return convertSvgToBlobUrl(data, IST_NAVY);
    };

    // Favorites stay gold
    if (!factory._ist_get_icon_url) {
      factory._ist_get_icon_url = factory.get_icon_url.bind(factory);
    }
    var origGet = factory._ist_get_icon_url;

    factory.get_icon_url = function (icon_name) {
      if (!icon_name) {
        return jQuery.when('');
      }
      var isFavorite =
        icon_name === 'tryton-star' || icon_name === 'tryton-star-border';
      if (!isFavorite) {
        return origGet(icon_name);
      }
      var cacheKey = icon_name + '@ist-gold';
      if (cacheKey in factory.loaded_icons) {
        return jQuery.when(factory.loaded_icons[cacheKey]);
      }
      return factory.register_icon(icon_name).then(function () {
        if (cacheKey in factory.loaded_icons) {
          return factory.loaded_icons[cacheKey];
        }
        return jQuery
          .get('images/' + icon_name + '.svg', null, null, 'text')
          .then(function (svgText) {
            var url = convertSvgToBlobUrl(svgText, IST_GOLD);
            factory.loaded_icons[cacheKey] = url;
            return url;
          });
      });
    };
  }

  function applyIstSaoTheme() {
    if (typeof Sao === 'undefined' || !Sao.config) {
      return false;
    }

    Sao.config.icon_colors = [IST_NAVY, IST_MUTED, IST_GOLD];
    Sao.config.calendar_colors = ['#ffffff', IST_NAVY];
    Sao.config.graph_color = IST_NAVY;
    Sao.config.title = 'IST';

    patchIconFactory();

    try {
      var titleEl = document.getElementById('title');
      if (titleEl && /tryton/i.test(titleEl.textContent || '')) {
        titleEl.textContent = 'IST';
      }
    } catch (eTitle) {
      /* ignore */
    }
    return true;
  }

  /** Login modal small subtitle: version → "IST HIS" (keep title "Login"). */
  function themeLoginDialogHeader(root) {
    try {
      var scope = root || document;
      var smalls = scope.querySelectorAll(
        '.login-dialog .modal-header .modal-title small'
      );
      for (var i = 0; i < smalls.length; i++) {
        var el = smalls[i];
        if (el.getAttribute('data-ist-login-sub') === '1') {
          continue;
        }
        el.setAttribute('data-ist-login-sub', '1');
        el.setAttribute('title', el.textContent || '');
        el.textContent = 'IST HIS';
      }
    } catch (eLogin) {
      /* ignore */
    }
  }

  function isFavoriteImg(img) {
    if (!img) {
      return false;
    }
    var cls = String(img.className || '');
    if (/\bfavorite/i.test(cls)) {
      return true;
    }
    var cell = img.closest && img.closest('td.favorite, .favorite');
    return !!cell;
  }

  function recolorBlobImg(img) {
    if (!img || img.getAttribute('data-ist-recolored') === '1') {
      return;
    }
    var src = img.getAttribute('src') || '';
    if (!src || (src.indexOf('blob:') !== 0 && src.indexOf('data:image/svg') !== 0)) {
      return;
    }
    var favor = isFavoriteImg(img);
    img.setAttribute('data-ist-recolored', '1');
    fetch(src)
      .then(function (r) {
        return r.text();
      })
      .then(function (svgText) {
        if (!svgText || svgText.indexOf('<svg') === -1) {
          return;
        }
        var target = favor ? IST_GOLD : IST_NAVY;
        // Recolor teal leftovers AND beige/flesh heads (Party, etc.)
        if (!svgNeedsIstRecolor(svgText, target)) {
          return;
        }
        var url = convertSvgToBlobUrl(svgText, target);
        img.setAttribute('src', url);
      })
      .catch(function () {
        img.removeAttribute('data-ist-recolored');
      });
  }

  function walkMenuIcons(root) {
    try {
      var scope = root && root.querySelectorAll ? root : document;
      var nodes = scope.querySelectorAll
        ? scope.querySelectorAll(
            '#menu img, .treeview img, img.icon, img.column-affix, img.favorite-icon, img.global_search-icon, #global-search img, .toolbar img.icon'
          )
        : [];
      for (var i = 0; i < nodes.length; i++) {
        recolorBlobImg(nodes[i]);
      }
      if (root && root.tagName === 'IMG') {
        recolorBlobImg(root);
      }
    } catch (eWalk) {
      /* ignore */
    }
  }

  function startIconObserver() {
    if (typeof MutationObserver === 'undefined') {
      return;
    }
    var obs = new MutationObserver(function (mutations) {
      for (var m = 0; m < mutations.length; m++) {
        var mut = mutations[m];
        if (mut.type === 'attributes' && mut.attributeName === 'src') {
          var t = mut.target;
          if (t && t.tagName === 'IMG' && t.getAttribute('data-ist-recolored') !== '1') {
            recolorBlobImg(t);
          }
          continue;
        }
        var nodes = mut.addedNodes;
        for (var n = 0; n < nodes.length; n++) {
          var node = nodes[n];
          if (!node || node.nodeType !== 1) {
            continue;
          }
          if (
            (node.classList && node.classList.contains('login-dialog')) ||
            (node.querySelector && node.querySelector('.login-dialog'))
          ) {
            themeLoginDialogHeader(node);
          }
          walkMenuIcons(node);
        }
      }
    });
    obs.observe(document.documentElement, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ['src'],
    });
  }

  try {
    document.documentElement.setAttribute('data-ist-theme', 'navy-gold');

    // Apply as early as possible (custom.js loads after tryton-sao.js)
    applyIstSaoTheme();
    themeLoginDialogHeader();
    startIconObserver();

    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', function () {
        applyIstSaoTheme();
        walkMenuIcons(document);
      });
    } else {
      walkMenuIcons(document);
    }

    // After login / menu paint — short sweeps for late-loaded icons
    var sweeps = 0;
    var sweepTimer = setInterval(function () {
      applyIstSaoTheme();
      walkMenuIcons(document);
      sweeps += 1;
      if (sweeps >= 24) {
        clearInterval(sweepTimer);
      }
    }, 500);

    if (window.self !== window.top) {
      document.documentElement.classList.add('ist-embedded');
      try {
        if (document.title && /tryton/i.test(document.title)) {
          document.title = document.title.replace(/tryton/gi, 'IST').trim();
        }
      } catch (e2) {
        /* ignore */
      }
      // Parent React app owns auth; if IST session vanished, bounce top to /login.
      try {
        if (!localStorage.getItem(IST_SESSION_KEY) && window.top) {
          window.top.location.href = '/login';
        }
      } catch (e3) {
        /* cross-origin — ignore */
      }
    }
  } catch (e) {
    /* ignore */
  }
})();
