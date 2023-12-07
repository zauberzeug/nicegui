from typing import Any, Dict, Optional

from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish

from nicegui import ui


class NiceGuiLogElementCallbackHandler(BaseCallbackHandler):
    """Callback Handler that writes to a log element."""

    def __init__(self, log_element: ui.log) -> None:
        """Initialize callback handler."""
        self.log = log_element

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we are entering a chain."""
        self.log.push(f'\n\n> Entering new {serialized["id"][-1]} chain...')

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        self.log.push('\n> Finished chain.')
        self.log.push(f'\nOutputs: {outputs}')

    def on_agent_action(self, action: AgentAction, **kwargs: Any) -> Any:
        """Run on agent action."""
        self.log.push(action.log)

    def on_tool_end(self,
                    output: str,
                    observation_prefix: Optional[str] = None,
                    llm_prefix: Optional[str] = None,
                    **kwargs: Any,
                    ) -> None:
        """If not the final action, print out observation."""
        if observation_prefix is not None:
            self.log.push(f'\n{observation_prefix}')
        self.log.push(output)
        if llm_prefix is not None:
            self.log.push(f'\n{llm_prefix}')

    def on_text(self, text: str, **kwargs: Any) -> None:
        """Run when agent ends."""
        self.log.push(text)

    def on_agent_finish(self, finish: AgentFinish, **kwargs: Any) -> None:
        """Run on agent end."""
        self.log.push(finish.log)
