# Codebase Review Spec

## Why
用户请求审阅当前工作空间下的代码。为了确保代码质量、发现潜在问题并提供优化建议，需要对现有的代码进行系统性的审查。

## What Changes
- 不修改现有代码（只读模式）
- 梳理工作空间下的 Python 代码库结构（主要是 RAG 和 Agent 相关项目）
- 分析代码架构、实现规范、错误处理以及潜在的优化空间
- 生成一份详尽的代码审阅报告

## Impact
- Affected specs: 无（仅审阅）
- Affected code: 无修改，仅读取分析

## ADDED Requirements
### Requirement: Code Review Report
系统应当提供一份当前目录下代码的审阅分析报告。

#### Scenario: Success case
- **WHEN** 完成代码读取与分析
- **THEN** 生成一份 Markdown 格式的审阅报告，包含架构概述、代码规范检查、亮点与改进建议。