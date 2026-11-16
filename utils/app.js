(function () {
  "use strict";

  var articles = Array.prototype.slice.call(document.querySelectorAll("[data-route]"));
  var navLinks = Array.prototype.slice.call(document.querySelectorAll("[data-nav]"));
  var byRoute = {};
  articles.forEach(function (el) { byRoute[el.getAttribute("data-route")] = el; });

  var baseTitle = document.title;
  var contentPane = document.querySelector(".main");

  function scrollContentTop() {
    if (contentPane) contentPane.scrollTop = 0;
  }
  var sidebar = document.getElementById("sidebar");
  var scrim = document.getElementById("scrim");
  var input = document.getElementById("search");
  var results = document.getElementById("results");
  var homeArt = document.querySelector(".ascii-art");

  /* --- theme -------------------------------------------------------------- */

  var themeButtons = Array.prototype.slice.call(
    document.querySelectorAll("[data-theme-set]")
  );

  function applyTheme(name) {
    if (name === "dark") {
      document.documentElement.setAttribute("data-theme", "dark");
    } else {
      document.documentElement.removeAttribute("data-theme");
    }
    themeButtons.forEach(function (b) {
      b.classList.toggle("active", b.getAttribute("data-theme-set") === name);
      b.setAttribute("aria-pressed", b.getAttribute("data-theme-set") === name);
    });
    try { localStorage.setItem("neuron-glossary-theme", name); } catch (e) {}
  }

  themeButtons.forEach(function (b) {
    b.addEventListener("click", function () {
      applyTheme(b.getAttribute("data-theme-set"));
    });
  });

  applyTheme(
    document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light"
  );

  /* --- routing ------------------------------------------------------------ */

  function routeFromHash() {
    var h = location.hash || "";
    if (h.indexOf("#/") !== 0) return null;
    return h.slice(2).replace(/\/$/, "");
  }

  function show(route) {
    var el = byRoute[route];
    if (!el) {
      el = byRoute[""];
      route = "";
    }
    articles.forEach(function (a) { a.hidden = a !== el; });
    if (!route && homeArt) {
      if (homeArt.animate && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
        homeArt.querySelectorAll("span").forEach(function (row, index) {
          row.animate(
            [{ clipPath: "inset(0 100% 0 0)" }, { clipPath: "inset(0 0% 0 0)" }],
            {
              delay: index * 32, duration: 480, fill: "backwards",
              easing: "steps(" + Math.max(1, row.textContent.length) + ", end)"
            }
          );
        });
      }
      homeArt = null;
    }
    navLinks.forEach(function (a) {
      a.classList.toggle("active", a.getAttribute("data-nav") === route);
    });
    var h1 = el.querySelector("h1");
    document.title = route && h1 ? h1.textContent + " — " + baseTitle : baseTitle;
    revealActive(route);
    closeSidebar();
  }

  // Keep the active link visible through every collapsed parent.
  function revealActive(route) {
    var link = document.querySelector('[data-nav="' + route + '"]');
    if (!link) return;
    var group = route ? link.closest(".nav-group[data-group]") : null;
    while (group) {
      if (group.classList.contains("collapsed")) setCollapsed(group, false);
      group = group.parentElement.closest(".nav-group[data-group]");
    }
    link.scrollIntoView({ block: "nearest" });
  }

  function onHashChange() {
    var route = routeFromHash();
    if (route === null) {
      // an in-page anchor: keep the current article and let the browser scroll
      if (location.hash && document.querySelector(location.hash)) return;
      show("");
      scrollContentTop();
      return;
    }
    show(route);
    scrollContentTop();
  }

  window.addEventListener("hashchange", onHashChange);

  /* --- collapsible nav sections ------------------------------------------- */

  var COLLAPSE_KEY = "neuron-glossary-collapsed";
  var groups = Array.prototype.slice.call(document.querySelectorAll(".nav-group[data-group]"));

  function readCollapsed() {
    try {
      var raw = localStorage.getItem(COLLAPSE_KEY);
      return raw ? JSON.parse(raw) : [];
    } catch (e) { return []; }
  }

  function writeCollapsed(list) {
    try { localStorage.setItem(COLLAPSE_KEY, JSON.stringify(list)); } catch (e) {}
  }

  function setCollapsed(group, collapsed) {
    var slug = group.getAttribute("data-group");
    var toggle = group.querySelector(":scope > .nav-head-row > .nav-toggle");
    group.classList.toggle("collapsed", collapsed);
    if (toggle) toggle.setAttribute("aria-expanded", collapsed ? "false" : "true");

    var list = readCollapsed().filter(function (s) { return s !== slug; });
    if (collapsed) list.push(slug);
    writeCollapsed(list);
  }

  var initiallyCollapsed = readCollapsed();
  groups.forEach(function (group) {
    var slug = group.getAttribute("data-group");
    var collapsed = initiallyCollapsed.indexOf(slug) !== -1;
    group.classList.toggle("collapsed", collapsed);
    var toggle = group.querySelector(":scope > .nav-head-row > .nav-toggle");
    if (!toggle) return;
    toggle.setAttribute("aria-expanded", collapsed ? "false" : "true");
    toggle.addEventListener("click", function (e) {
      e.preventDefault();
      setCollapsed(group, !group.classList.contains("collapsed"));
    });
  });

  /* --- sidebar ------------------------------------------------------------ */

  function closeSidebar() {
    sidebar.classList.remove("open");
    if (scrim) scrim.classList.remove("open");
  }

  document.getElementById("menu-toggle").addEventListener("click", function () {
    sidebar.classList.toggle("open");
    if (scrim) scrim.classList.toggle("open", sidebar.classList.contains("open"));
  });
  if (scrim) scrim.addEventListener("click", closeSidebar);

  /* --- search ------------------------------------------------------------- */

  var INDEX = window.__GLOSSARY_INDEX__ || [];
  var selected = -1;
  var current = [];

  function score(entry, q) {
    var title = entry.t.toLowerCase();
    var abbr = (entry.a || "").toLowerCase();
    if (title === q || abbr === q) return 0;
    if (abbr && abbr.indexOf(q) === 0) return 1;
    if (title.indexOf(q) === 0) return 1;
    var word = title.split(/[\s(),/-]+/).some(function (w) { return w.indexOf(q) === 0; });
    if (word) return 2;
    if (title.indexOf(q) !== -1) return 3;
    if (entry.b.toLowerCase().indexOf(q) !== -1) return 4;
    return -1;
  }

  function search(q) {
    q = q.trim().toLowerCase();
    if (!q) return [];
    var hits = [];
    for (var i = 0; i < INDEX.length; i++) {
      var s = score(INDEX[i], q);
      if (s >= 0) hits.push({ e: INDEX[i], s: s });
    }
    hits.sort(function (a, b) { return a.s - b.s || a.e.t.length - b.e.t.length; });
    return hits.slice(0, 12).map(function (h) { return h.e; });
  }

  function renderResults(list) {
    current = list;
    selected = -1;
    if (!list.length) {
      results.innerHTML =
        '<div class="results-inner"><div class="r-none">No matching terms.</div></div>';
      results.hidden = false;
      return;
    }
    var html = list
      .map(function (e) {
        var chip = e.a ? '<span class="chip">' + e.a + "</span>" : "";
        return (
          '<a href="#/' + e.p + '"><span class="r-sec">' + e.s +
          '</span><span class="r-title">' + e.t + "</span>" + chip + "</a>"
        );
      })
      .join("");
    results.innerHTML = '<div class="results-inner">' + html + "</div>";
    results.hidden = false;
  }

  function clearResults() {
    results.hidden = true;
    results.innerHTML = "";
    current = [];
    selected = -1;
  }

  function moveSelection(delta) {
    if (!current.length) return;
    var links = results.querySelectorAll("a");
    if (selected >= 0 && links[selected]) links[selected].classList.remove("sel");
    selected = (selected + delta + current.length) % current.length;
    links[selected].classList.add("sel");
    links[selected].scrollIntoView({ block: "nearest" });
  }

  input.addEventListener("input", function () {
    var q = input.value;
    if (!q.trim()) { clearResults(); return; }
    renderResults(search(q));
  });

  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); moveSelection(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); moveSelection(-1); }
    else if (e.key === "Enter") {
      var links = results.querySelectorAll("a");
      var target = selected >= 0 ? links[selected] : links[0];
      if (target) {
        e.preventDefault();
        location.hash = target.getAttribute("href");
        input.value = "";
        input.blur();
        clearResults();
      }
    } else if (e.key === "Escape") {
      input.value = "";
      input.blur();
      clearResults();
    }
  });

  results.addEventListener("click", function (e) {
    if (e.target.closest("a")) { input.value = ""; clearResults(); }
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".search-wrap")) clearResults();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "/" && document.activeElement !== input) {
      e.preventDefault();
      input.focus();
      input.select();
    }
  });

  onHashChange();
})();
