from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish
from typing import Dict, Any, Optional
from nicegui.element import Element


class NiceGuiLogElementCallbackHandler(BaseCallbackHandler):
    """Callback Handler that writes to the log element of NicGui."""

    def __init__(self, element: Element) -> None:
        """Initialize callback handler."""
        self.element = element

    def print_text(self, message: str) -> None:
        self.element.push(message)
        self.element.update()

    def on_chain_start(
        self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any
    ) -> None:
        """Print out that we are entering a chain."""
        self.print_text(
            f"\n\n> Entering new {serialized['id'][-1]} chain...",
        )

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        self.print_text("\n> Finished chain.")
        self.print_text(f"\nOutputs: {outputs}")

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        self.print_text(action.log)

    def on_tool_end(
        self,
        output: str,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        if observation_prefix is not None:
            self.print_text(f"\n{observation_prefix}")
        self.print_text(output)
        if llm_prefix is not None:
            self.print_text(f"\n{llm_prefix}")

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Run when agent ends."""
        self.print_text(text)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""
        self.print_text(finish.log)
