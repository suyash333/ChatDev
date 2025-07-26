#!/usr/bin/env python3
"""
Code quality and security check script for ChatDev.
Run this script to perform basic code quality checks.
"""

import os
import re
import ast
import sys
from pathlib import Path


def check_security_issues(file_path):
    """Check for potential security issues in Python files."""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for shell=True usage
        if 'shell=True' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'shell=True' in line:
                    issues.append(f"Line {i}: Potential shell injection risk (shell=True)")
        
        # Check for eval/exec usage
        if re.search(r'\b(eval|exec)\s*\(', content):
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if re.search(r'\b(eval|exec)\s*\(', line):
                    issues.append(f"Line {i}: Dangerous function usage (eval/exec)")
        
        # Check for hardcoded secrets patterns
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]
        
        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append(f"Potential hardcoded secret found")
                
    except Exception as e:
        issues.append(f"Error reading file: {e}")
        
    return issues


def check_code_quality(file_path):
    """Check for code quality issues."""
    issues = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        lines = content.split('\n')
        
        # Check for long lines
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                issues.append(f"Line {i}: Line too long ({len(line)} characters)")
        
        # Check for broad exception handling
        for i, line in enumerate(lines, 1):
            if re.search(r'except\s*:', line):
                issues.append(f"Line {i}: Broad exception handling (except:)")
        
        # Check for missing docstrings in functions/classes
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
                    if not ast.get_docstring(node):
                        issues.append(f"Line {node.lineno}: Missing docstring for {node.name}")
        except SyntaxError as e:
            issues.append(f"Syntax error: {e}")
            
    except Exception as e:
        issues.append(f"Error analyzing file: {e}")
        
    return issues


def check_file(file_path):
    """Check a single Python file for issues."""
    print(f"\nChecking: {file_path}")
    
    security_issues = check_security_issues(file_path)
    quality_issues = check_code_quality(file_path)
    
    if security_issues:
        print("  🔒 Security Issues:")
        for issue in security_issues:
            print(f"    - {issue}")
    
    if quality_issues:
        print("  📝 Code Quality Issues:")
        for issue in quality_issues[:5]:  # Limit to first 5 to avoid spam
            print(f"    - {issue}")
        if len(quality_issues) > 5:
            print(f"    ... and {len(quality_issues) - 5} more issues")
    
    if not security_issues and not quality_issues:
        print("  ✅ No issues found")
        
    return len(security_issues), len(quality_issues)


def main():
    """Main function to run code quality checks."""
    print("ChatDev Code Quality & Security Check")
    print("=" * 40)
    
    # Find all Python files in chatdev directory
    chatdev_dir = Path(__file__).parent.parent / "chatdev"
    python_files = list(chatdev_dir.glob("*.py"))
    
    if not python_files:
        print("No Python files found in chatdev directory")
        return
    
    total_security_issues = 0
    total_quality_issues = 0
    
    for file_path in python_files:
        security_count, quality_count = check_file(file_path)
        total_security_issues += security_count
        total_quality_issues += quality_count
    
    print(f"\n" + "=" * 40)
    print(f"Summary:")
    print(f"  🔒 Total Security Issues: {total_security_issues}")
    print(f"  📝 Total Code Quality Issues: {total_quality_issues}")
    
    if total_security_issues > 0:
        print(f"\n⚠️  Please address security issues before deployment!")
        sys.exit(1)
    elif total_quality_issues > 10:
        print(f"\n💡 Consider addressing code quality issues for better maintainability")
    else:
        print(f"\n✅ Code quality looks good!")


if __name__ == "__main__":
    main()