/* ADRE front-end – Aero + hacker aesthetic */

(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const logbox = $("logbox");

  function log(msg) {
    const t = new Date().toTimeString().slice(0, 8);
    logbox.textContent += "[" + t + "] " + msg + "\n";
    logbox.scrollTop = logbox.scrollHeight;
  }

  function setStatus(msg) {
    $("status-left").textContent = msg;
  }

  const cy = cytoscape({
    container: $("cy-container"),
    style: [
      {
        selector: "node",
        style: {
          "background-color": "#1a3a5a",
          "border-width": 1.5,
          "border-color": "#4a90c8",
          "label": "data(label)",
          "color": "#c0e0ff",
          "font-family": "Consolas, monospace",
          "font-size": 10,
          "text-valign": "bottom",
          "text-margin-y": 4,
          "width": 26,
          "height": 26,
          "text-outline-width": 2,
          "text-outline-color": "#050a12"
        }
      },
      {
        selector: "node[kind='module']",
        style: {
          "background-color": "#1a4a3a",
          "border-color": "#40c080",
          "shape": "round-rectangle",
          "width": 36,
          "height": 28
        }
      },
      {
        selector: "node:selected",
        style: {
          "background-color": "#33cc66",
          "border-color": "#a0ffa0",
          "border-width": 2.5,
          "color": "#001a08",
          "text-outline-color": "#33cc66"
        }
      },
      {
        selector: "edge",
        style: {
          "width": 1.4,
          "line-color": "#3a5a7a",
          "target-arrow-color": "#3a5a7a",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
          "arrow-scale": 0.7,
          "opacity": 0.85
        }
      },
      {
        selector: "edge[kind='imports']",
        style: {
          "line-color": "#5a80a0",
          "target-arrow-color": "#5a80a0"
        }
      },
      {
        selector: "edge[kind='calls']",
        style: {
          "line-color": "#40a060",
          "target-arrow-color": "#40a060",
          "width": 1.6
        }
      },
      {
        selector: "edge:selected, .highlighted",
        style: {
          "line-color": "#33ccff",
          "target-arrow-color": "#33ccff",
          "width": 2.2,
          "opacity": 1
        }
      },
      {
        selector: "node.highlighted",
        style: {
          "border-color": "#33ccff",
          "border-width": 2.5
        }
      }
    ],
    layout: { name: "cose", animate: false, padding: 40, nodeRepulsion: 8000 },
    minZoom: 0.2,
    maxZoom: 3,
    wheelSensitivity: 0.3
  });

  const demoElements = [
    { data: { id: "core", label: "core.py", kind: "module" } },
    { data: { id: "services", label: "services.py", kind: "module" } },
    { data: { id: "utils", label: "utils.py", kind: "module" } },
    { data: { id: "state", label: "state.py", kind: "module" } },
    { data: { id: "config", label: "config.py", kind: "module" } },
    { data: { id: "main", label: "main.py", kind: "module" } },
    { data: { id: "core.init_core", label: "init_core()", kind: "function" } },
    { data: { id: "core.process_request", label: "process_request()", kind: "function" } },
    { data: { id: "services.handle", label: "handle()", kind: "function" } },
    { data: { id: "services.register_handler", label: "register_handler()", kind: "function" } },
    { data: { id: "utils.helper", label: "helper()", kind: "function" } },
    { data: { id: "e1", source: "core", target: "services", kind: "imports" } },
    { data: { id: "e2", source: "services", target: "core", kind: "imports" } },
    { data: { id: "e3", source: "core", target: "utils", kind: "imports" } },
    { data: { id: "e4", source: "core", target: "state", kind: "imports" } },
    { data: { id: "e5", source: "core", target: "config", kind: "imports" } },
    { data: { id: "e6", source: "services", target: "utils", kind: "imports" } },
    { data: { id: "e7", source: "services", target: "state", kind: "imports" } },
    { data: { id: "e8", source: "main", target: "core", kind: "imports" } },
    { data: { id: "e9", source: "core.process_request", target: "services.handle", kind: "calls" } },
    { data: { id: "e10", source: "services.handle", target: "core.init_core", kind: "calls" } },
    { data: { id: "e11", source: "core.init_core", target: "services.register_handler", kind: "calls" } },
    { data: { id: "e12", source: "core.init_core", target: "utils.helper", kind: "calls" } },
    { data: { id: "e13", source: "services.handle", target: "utils.helper", kind: "calls" } }
  ];

  function loadGraph(elements) {
    cy.elements().remove();
    cy.add(elements);
    cy.layout({ name: "cose", animate: false, padding: 40, nodeRepulsion: 9000 }).run();
    $("node-count").textContent = cy.nodes().length;
    $("edge-count").textContent = cy.edges().length;
    rebuildList();
    log("graph loaded – " + cy.nodes().length + " nodes, " + cy.edges().length + " edges");
    setStatus("Graph loaded");
  }

  function rebuildList() {
    const list = $("func-list");
    list.innerHTML = "";
    cy.nodes().forEach(function (n) {
      const div = document.createElement("div");
      div.className = "list-item";
      div.dataset.id = n.id();
      const kind = n.data("kind") || "";
      div.innerHTML = (n.data("label") || n.id()) + '<span class="kind">' + kind + "</span>";
      div.addEventListener("click", function () {
        cy.elements().unselect();
        n.select();
        cy.center(n);
        highlight(n);
        updateSelection(n);
      });
      list.appendChild(div);
    });
  }

  function highlight(node) {
    cy.elements().removeClass("highlighted");
    node.neighborhood().addClass("highlighted");
    node.addClass("highlighted");
  }

  function updateSelection(node) {
    $("sel-id").textContent = node.id();
    $("sel-kind").textContent = node.data("kind") || "\u2014";
    $("sel-label").textContent = node.data("label") || node.id();
    $("sel-degree").textContent = "in:" + node.indegree() + "  out:" + node.outdegree();
    document.querySelectorAll(".list-item").forEach(function (el) {
      el.classList.toggle("active", el.dataset.id === node.id());
    });
  }

  cy.on("tap", "node", function (evt) {
    const node = evt.target;
    highlight(node);
    updateSelection(node);
    setStatus("Selected " + node.id());
  });

  cy.on("tap", function (evt) {
    if (evt.target === cy) {
      cy.elements().removeClass("highlighted");
      $("sel-id").textContent = "--------";
      $("sel-kind").textContent = "--------";
      $("sel-label").textContent = "--------";
      $("sel-degree").textContent = "in:0  out:0";
      document.querySelectorAll(".list-item").forEach(function (el) {
        el.classList.remove("active");
      });
      setStatus("Ready");
    }
  });

  $("btn-fit").addEventListener("click", function () {
    cy.fit(50);
    setStatus("Fit");
  });
  $("btn-layout").addEventListener("click", function () {
    cy.layout({ name: "cose", animate: true, animationDuration: 500, padding: 40 }).run();
    setStatus("Layout");
  });
  $("btn-reload").addEventListener("click", function () {
    loadGraph(demoElements);
  });
  $("btn-open").addEventListener("click", function () {
    log("Open Graph – file dialog not wired (Phase 1)");
    setStatus("Open not wired yet");
  });
  $("btn-agent").addEventListener("click", function () {
    const sel = cy.$("node:selected");
    if (sel.empty()) {
      log("no selection – pick a node first");
      setStatus("No selection");
      return;
    }
    const id = sel[0].id();
    const corr = "corr-" + Date.now().toString(36);
    $("corr-id").textContent = corr;
    $("rea-status").textContent = "agent context packaged";
    log("Send->Agent  node=" + id + "  " + corr);
    setStatus("Agent hand-off (stub)");
  });
  $("btn-rea").addEventListener("click", function () {
    const sel = cy.$("node:selected");
    if (sel.empty()) {
      log("select a node before REA query");
      return;
    }
    $("rea-status").textContent = "REA stub – client not connected";
    log("REA query  " + sel[0].id() + "  (stub)");
    setStatus("REA query stub");
  });

  loadGraph(demoElements);
  $("status-right").textContent = "REA: offline";
  log("ADRE control plane online");
  log("theme: Aero glass + phosphor");
  log("demo graph = hello_world cycle (core <-> services)");
})();
