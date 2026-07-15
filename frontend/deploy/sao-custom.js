/**
 * IST HIS optional tweaks for GNU Health SAO.
 * Deploy to SAO web root as custom.js (auto-loaded by SAO after tryton-sao.js).
 * Keep minimal — do not break wizards or JSON-RPC.
 *
 * Icon colors: SAO paints SVG fills from Sao.config.icon_colors[0] in
 * ICONFACTORY._convert (default teal #267f82). Override here — CSS alone cannot
 * recolor data:/blob SVG img icons reliably.
 */
(function () {
  'use strict';

  var IST_NAVY = '#0a1f44';
  var IST_MUTED = '#3d4f6a';
  var IST_GOLD = '#c9a66b';

  function applyIstSaoTheme() {
    if (typeof Sao === 'undefined' || !Sao.config) {
      return;
    }

    // Primary = navy (menu/action icons); secondary = muted; tertiary = gold
    Sao.config.icon_colors = [IST_NAVY, IST_MUTED, IST_GOLD];
    Sao.config.calendar_colors = ['#ffffff', IST_NAVY];
    Sao.config.graph_color = IST_NAVY;
    Sao.config.title = 'IST';

    // Prefer gold for favorite stars (still go through ICONFACTORY._convert)
    if (Sao.common && Sao.common.ICONFACTORY) {
      var factory = Sao.common.ICONFACTORY;
      var origGet = factory.get_icon_url.bind(factory);

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
              var xml = jQuery.parseXML(svgText);
              jQuery(xml).find('svg').attr('fill', IST_GOLD);
              var serialized = new XMLSerializer().serializeToString(xml);
              var url = window.URL.createObjectURL(
                new Blob([serialized], { type: 'image/svg+xml' })
              );
              factory.loaded_icons[cacheKey] = url;
              return url;
            });
        });
      };
    }

    // Soften brand text if SAO already painted #title
    try {
      var titleEl = document.getElementById('title');
      if (titleEl && /tryton/i.test(titleEl.textContent || '')) {
        titleEl.textContent = 'IST';
      }
    } catch (eTitle) {
      /* ignore */
    }
  }

  try {
    document.documentElement.setAttribute('data-ist-theme', 'navy-gold');
    applyIstSaoTheme();

    // Soften document title / brand when embedded (IST Workspace iframe)
    if (window.self !== window.top) {
      document.documentElement.classList.add('ist-embedded');
      try {
        if (document.title && /tryton/i.test(document.title)) {
          document.title = document.title.replace(/tryton/gi, 'IST').trim();
        }
      } catch (e2) {
        /* ignore */
      }
    }
  } catch (e) {
    /* ignore */
  }
})();
