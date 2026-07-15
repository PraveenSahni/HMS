/**
 * IST HIS optional tweaks for GNU Health SAO.
 * Deploy to SAO web root as custom.js (auto-loaded by SAO).
 * Keep minimal — do not break wizards or JSON-RPC.
 */
(function () {
  'use strict';
  try {
    document.documentElement.setAttribute('data-ist-theme', 'navy-gold');
    // Soften document title when embedded (IST Workspace iframe)
    if (window.self !== window.top) {
      document.documentElement.classList.add('ist-embedded');
    }
  } catch (e) {
    /* ignore */
  }
})();
