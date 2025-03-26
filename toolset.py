# plugins/openmanus/toolset.py
import argparse
import asyncio
import sys
import os
import re
import json

import typing as t

from typing import List, cast

# Import from run_mcp
from run_mcp import MCPRunner

# Import from Composio
from composio import ComposioToolSet as BaseComposioToolSet
from composio.tools import ComposioToolSet as BaseComposioToolSet
from composio.tools.toolset import ProcessorsType
from composio.utils.pydantic import parse_pydantic_error
from composio.utils.shared import get_signature_format_from_schema_params

# Import from your target framework
from app.agent.mcp import MCPAgent
from app.config import config
from app.logger import logger


class OpenManusToolSet(BaseComposioToolSet):
    def __init__(self, *args, **kwargs):
        # 设置 API 密钥
        kwargs['api_key'] = "your_api_key"  # 替换为你的实际 Composio API 密钥
        super().__init__(*args, **kwargs)
        self.runner = MCPRunner()
        self._init_client()

    async def run_interactive(self, params):
        """
        Run OpenManus in interactive mode.
        """
        await self.runner.initialize("stdio")
        await self.runner.run_interactive()
        await self.runner.cleanup()

    async def run_single_prompt(self, params):
        """
        Run OpenManus with a single prompt.
        """
        await self.runner.initialize("stdio")
        await self.runner.run_single_prompt(params.get("prompt", ""))
        await self.runner.cleanup()

    def get_tools(self):
        """
        Return a list of tools available in this toolset.
        """
        return [
            {
                "name": "run_interactive",
                "description": "Run OpenManus in interactive mode",
                "func": self.run_interactive,
            },
            {
                "name": "run_single_prompt",
                "description": "Run OpenManus with a single prompt",
                "func": self.run_single_prompt,
            },
        ]

    def _wrap_tool(self, tool):
        """
        Wrap the tool function to match Composio's expectations.
        """
        async def wrapped_tool(params):
            # Convert params to the format expected by OpenManus
            formatted_params = self._format_params(params)
            result = await tool(formatted_params)
            # Convert the result to a string (if needed)
            return self._format_result(result)
        return wrapped_tool

    def _format_params(self, params):
        """
        Format the parameters to match OpenManus's expectations.
        """
        # Example transformation (adjust as needed)
        formatted_params = {k: v for k, v in params.items()}
        return formatted_params

    def _format_result(self, result):
        """
        Format the result to match Composio's expectations.
        """
        # Example transformation (adjust as needed)
        if isinstance(result, dict):
            return json.dumps(result)
        return result