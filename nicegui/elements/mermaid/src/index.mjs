// mermaid calls `selection.transition()`, which only this import registers (d3 itself is marked as side-effect-free)
import "d3-transition";
export { default as mermaid } from "mermaid";
