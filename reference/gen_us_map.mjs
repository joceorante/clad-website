// Builds src/data/us-states.json (one SVG path per state, 975x610 Albers USA) from the us-atlas package.
// Run from a folder that has us-atlas@3, topojson-client@3 and d3-geo@3 installed:
//   node /path/to/clad-site/reference/gen_us_map.mjs /path/to/clad-site/src/data/us-states.json
import { readFileSync, writeFileSync } from "node:fs";
import { createRequire } from "node:module";
import { join } from "node:path";
const require = createRequire(join(process.cwd(), "noop.js"));
const { feature } = require("topojson-client");
const { geoPath } = require("d3-geo");
const topo = JSON.parse(readFileSync(require.resolve("us-atlas/states-albers-10m.json"), "utf8"));
const path = geoPath();
const round = (d) => d.replace(/\d+\.\d+/g, (n) => (+n).toFixed(1));
const states = feature(topo, topo.objects.states).features
  .map((f) => ({ id: f.id, name: f.properties.name, d: round(path(f)) }))
  .sort((a, b) => a.id.localeCompare(b.id));
writeFileSync(process.argv[2], JSON.stringify(states));
console.log(states.length, "states");
