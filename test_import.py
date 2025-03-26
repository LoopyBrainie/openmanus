# plugins/openmanus/test_import.py
import sys
import os
import asyncio

# 添加当前目录到 sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from openmanus import OpenManusToolSet

async def test_run_single_prompt():
    toolset = OpenManusToolSet()
    prompt = "What is the weather like today?"
    print(f"Running single prompt: {prompt}")
    await toolset.run_single_prompt({"prompt": prompt})

async def test_run_interactive():
    toolset = OpenManusToolSet()
    print("Running interactive mode. Type 'exit' to quit.")
    await toolset.run_interactive({})

if __name__ == "__main__":
    # 测试单次提示模式
    print("Testing single prompt mode...")
    asyncio.run(test_run_single_prompt())

    # 测试交互模式
    print("\nTesting interactive mode...")
    asyncio.run(test_run_interactive())