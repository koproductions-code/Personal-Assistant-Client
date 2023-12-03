#!/usr/bin/env python3

import os
import argparse
from models.Llama2 import Llama2_Model
from models.GlaiveAI import GlaiveAI_Model
from clients.cli_client import CLIClient

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Client for LLM Smarthome Assistant.", description="This is a client for the LLM Smarthome Assistant")

    parser.add_argument("-u", "--host", default="0.0.0.0")
    parser.add_argument("-p", "--port", default=8000)
    parser.add_argument("-m", "--model", default="llama2") # glaiveai, llama2
    parser.add_argument("-c", "--config", default="../config/llama2")
    
    args = parser.parse_args()

    if not(os.path.exists(args.config)):
        raise RuntimeError(f"The config directory {args.config} does not exist.")

    if args.model == "glaiveai":
        model = GlaiveAI_Model()
    else:
        model = Llama2_Model()

    client = CLIClient(args.host, args.port, args.config, model)
    client.main()
    
    print("Goodbye!")