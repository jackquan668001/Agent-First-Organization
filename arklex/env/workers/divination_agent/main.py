#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from divination_agent import DivinationAgent

def main():
    """
    Command-Line Tool for I Ching Divination
    """
    parser = argparse.ArgumentParser(description="I Ching Divination Agent")
    parser.add_argument("--api_key", type=str, help="OpenAI API密钥")
    parser.add_argument("--numbers", type=str, help="6-digit number (e.g. 385962)")
    parser.add_argument("--query", type=str, default="Teavel", help="Inquiry type (e.g. Travel, Love, Career, Study)")
    
    args = parser.parse_args()
    
    # 获取API密钥
    api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        api_key = input("请输入OpenAI API密钥：")
    
    # 初始化Agent
    agent = DivinationAgent(api_key=api_key)
    

    
    # 获取数字
    numbers = args.numbers
    if not numbers:
        print("\nPlease choose an option:")
        print("1. Auto-cast hexagram (generate random number)")
        print("2. 2. Manually input a 6-digit number")
        choice = input("Enter your choice (1 or 2):")
        
        if choice == "1":
            numbers = None  # 自动生成
        else:
            while True:
                numbers = input("Please enter a 6-digit number:")
                if len(numbers) == 6 and numbers.isdigit():
                    break
                print("Invalid input. Please enter a valid 6-digit number.")
    
    # 获取问事方向
    query = args.query
    if not args.query:
        print("\nPlease select your inquiry direction:")
        print("1. Travel")
        print("2. Love")
        print("3. Career")
        print("4. Study")
        print("5. Custom")

        direction_choice = input("Enter your choice (1-5): ")

        if direction_choice == "1":
            query = "Travel"
        elif direction_choice == "2":
            query = "Love"
        elif direction_choice == "3":
            query = "Career"
        elif direction_choice == "4":
            query = "Study"
        else:
            query = input("Please enter your custom inquiry: ")
    
    # 进行占卜
    print("\nInterpreting the hexagram, please wait...\n")
    result = agent.divine(numbers=numbers, query=query)
    
    # 输出结果
    print(result)

if __name__ == "__main__":
    main()