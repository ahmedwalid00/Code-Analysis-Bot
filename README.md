# Code Analysis Bot using LangChain RAG Pipeline

This project implements a smart **Code Analysis Bot** designed to help users understand and explore source code using a custom RAG (Retrieval-Augmented Generation) pipeline. It utilizes a modular LangChain setup to retrieve code chunks and provide context-aware answers.

## Project Overview

The bot reads source code files, breaks them down into manageable chunks, retrieves relevant sections for a given query, and uses a conversational chain to respond intelligently.

It is built using a **custom chain class**, multiple LangChain Expression Language (LCEL) chains, and memory to retain conversation history. This design allows the bot to walk users through codebases and provide meaningful insights step-by-step.

## Technologies & Tools Used

- **LangChain**: Core framework for chaining LLMs and retrieval tools together.
- **Custom LCEL Chains**: Tailored chains for initial response and refinement.
- **Retrieval-Augmented Generation (RAG)**: Combines retrieval with generation for better code comprehension.
- **Python**: Main programming language.
- **LangChain Memory**: Keeps conversational context between queries.
- **Custom Retriever Module**: Built for efficient document chunking and vector retrieval.

## Features

- Conversational code explanation using memory-enhanced dialogue.
- Refined step-by-step answers tailored to user queries.
- Modular and scalable pipeline using LangChain components.
- Supports a wide range of code-related questions from documentation to logic tracing.

---

