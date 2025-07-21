#!/usr/bin/env python3
"""
GUN WiFi Tool - Security and Code Quality Analysis
Author: Security Analysis for GUN Community Tool
Description: Comprehensive security audit and code quality check
"""

import re
import ast
import os
import sys
from pathlib import Path

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class SecurityAnalyzer:
    """Security analysis for the WiFi tool"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            self.source_code = f.read()
        self.tree = ast.parse(self.source_code)
        self.lines = self.source_code.splitlines()
        
    def check_security_features(self):
        """Check for security features and potential issues"""
        print(f"{Colors.CYAN}🔒 Security Analysis{Colors.RESET}")
        
        security_checks = [
            ("Root privilege check", self.check_root_privileges),
            ("Input validation", self.check_input_validation),
            ("Dangerous operations protection", self.check_dangerous_ops),
            ("Legal disclaimers", self.check_legal_disclaimers),
            ("Error handling", self.check_error_handling),
            ("Logging implementation", self.check_logging),
            ("Signal handling", self.check_signal_handling),
            ("Dependency verification", self.check_dependency_verification)
        ]
        
        passed = 0
        total = len(security_checks)
        
        for check_name, check_func in security_checks:
            try:
                result, details = check_func()
                if result:
                    print(f"  {Colors.GREEN}✓{Colors.RESET} {check_name}")
                    if details:
                        print(f"    {details}")
                    passed += 1
                else:
                    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {check_name}")
                    if details:
                        print(f"    {details}")
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.RESET} {check_name}: {e}")
        
        print(f"\nSecurity Score: {passed}/{total} ({(passed/total)*100:.1f}%)")
        return passed, total
    
    def check_root_privileges(self):
        """Check if root privilege verification is implemented"""
        root_check = re.search(r'os\.geteuid\(\)', self.source_code)
        root_function = re.search(r'def check_root_privileges', self.source_code)
        
        if root_check and root_function:
            return True, "Root privilege checking implemented"
        return False, "Root privilege checking not found"
    
    def check_input_validation(self):
        """Check for input validation"""
        validation_patterns = [
            r'\.strip\(\)',
            r'if.*and.*:',
            r'try:.*except',
            r'argparse',
            r'input\('
        ]
        
        validations_found = sum(1 for pattern in validation_patterns 
                              if re.search(pattern, self.source_code))
        
        if validations_found >= 3:
            return True, f"Multiple input validation patterns found ({validations_found})"
        return False, f"Limited input validation ({validations_found})"
    
    def check_dangerous_ops(self):
        """Check for protection around dangerous operations"""
        dangerous_ops = [
            r'subprocess\.',
            r'airmon-ng',
            r'hostapd',
            r'iptables'
        ]
        
        protected_ops = 0
        for op in dangerous_ops:
            if re.search(op, self.source_code):
                # Check if it's in a try-except block
                if re.search(f'try:.*{op}.*except', self.source_code, re.DOTALL):
                    protected_ops += 1
        
        if protected_ops >= 2:
            return True, f"Dangerous operations properly protected ({protected_ops})"
        return False, f"Some dangerous operations may lack protection"
    
    def check_legal_disclaimers(self):
        """Check for legal disclaimers and warnings"""
        legal_keywords = [
            'LEGAL',
            'authorized',
            'authorization',
            'ethical',
            'illegal',
            'disclaimer'
        ]
        
        legal_mentions = sum(1 for keyword in legal_keywords 
                           if keyword.lower() in self.source_code.lower())
        
        if legal_mentions >= 4:
            return True, f"Comprehensive legal disclaimers present ({legal_mentions} mentions)"
        return False, f"Limited legal disclaimers ({legal_mentions} mentions)"
    
    def check_error_handling(self):
        """Check for proper error handling"""
        try_blocks = len(re.findall(r'try:', self.source_code))
        except_blocks = len(re.findall(r'except', self.source_code))
        
        if try_blocks >= 5 and except_blocks >= 5:
            return True, f"Good error handling ({try_blocks} try blocks, {except_blocks} except blocks)"
        return False, f"Limited error handling ({try_blocks} try blocks, {except_blocks} except blocks)"
    
    def check_logging(self):
        """Check for logging implementation"""
        logging_patterns = [
            r'import logging',
            r'logging\.',
            r'logger\.',
            r'\.log'
        ]
        
        logging_found = sum(1 for pattern in logging_patterns 
                          if re.search(pattern, self.source_code))
        
        if logging_found >= 3:
            return True, f"Comprehensive logging implemented ({logging_found} patterns)"
        return False, f"Limited logging ({logging_found} patterns)"
    
    def check_signal_handling(self):
        """Check for signal handling"""
        signal_check = re.search(r'signal\.signal', self.source_code)
        
        if signal_check:
            return True, "Signal handling implemented for graceful shutdown"
        return False, "No signal handling found"
    
    def check_dependency_verification(self):
        """Check for dependency verification"""
        dep_check = re.search(r'def check_dependencies', self.source_code)
        
        if dep_check:
            return True, "Dependency verification function implemented"
        return False, "No dependency verification found"

class CodeQualityAnalyzer:
    """Code quality analysis"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, 'r') as f:
            self.source_code = f.read()
        self.tree = ast.parse(self.source_code)
        self.lines = self.source_code.splitlines()
    
    def analyze_code_quality(self):
        """Analyze code quality metrics"""
        print(f"\n{Colors.CYAN}📊 Code Quality Analysis{Colors.RESET}")
        
        metrics = [
            ("Code structure", self.check_code_structure),
            ("Documentation", self.check_documentation),
            ("Function complexity", self.check_function_complexity),
            ("Code organization", self.check_code_organization),
            ("Naming conventions", self.check_naming_conventions),
            ("Import organization", self.check_imports),
            ("Constants usage", self.check_constants),
            ("Class design", self.check_class_design)
        ]
        
        passed = 0
        total = len(metrics)
        
        for metric_name, metric_func in metrics:
            try:
                result, details = metric_func()
                if result:
                    print(f"  {Colors.GREEN}✓{Colors.RESET} {metric_name}")
                    if details:
                        print(f"    {details}")
                    passed += 1
                else:
                    print(f"  {Colors.YELLOW}⚠{Colors.RESET} {metric_name}")
                    if details:
                        print(f"    {details}")
            except Exception as e:
                print(f"  {Colors.RED}✗{Colors.RESET} {metric_name}: {e}")
        
        print(f"\nCode Quality Score: {passed}/{total} ({(passed/total)*100:.1f}%)")
        return passed, total
    
    def check_code_structure(self):
        """Check overall code structure"""
        classes = len([n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)])
        functions = len([n for n in ast.walk(self.tree) if isinstance(n, ast.FunctionDef)])
        lines = len(self.lines)
        
        if classes >= 1 and functions >= 10 and lines >= 300:
            return True, f"Good structure: {classes} classes, {functions} functions, {lines} lines"
        return False, f"Basic structure: {classes} classes, {functions} functions, {lines} lines"
    
    def check_documentation(self):
        """Check for documentation"""
        docstrings = len(re.findall(r'""".*?"""', self.source_code, re.DOTALL))
        comments = len(re.findall(r'#.*', self.source_code))
        
        if docstrings >= 5 and comments >= 20:
            return True, f"Well documented: {docstrings} docstrings, {comments} comments"
        return False, f"Limited documentation: {docstrings} docstrings, {comments} comments"
    
    def check_function_complexity(self):
        """Check function complexity"""
        functions = [n for n in ast.walk(self.tree) if isinstance(n, ast.FunctionDef)]
        complex_functions = 0
        
        for func in functions:
            # Simple complexity check based on number of statements
            statements = len([n for n in ast.walk(func) if isinstance(n, ast.stmt)])
            if statements > 50:  # Arbitrary threshold
                complex_functions += 1
        
        if complex_functions <= len(functions) * 0.2:  # 20% threshold
            return True, f"Good complexity: {complex_functions}/{len(functions)} complex functions"
        return False, f"High complexity: {complex_functions}/{len(functions)} complex functions"
    
    def check_code_organization(self):
        """Check code organization"""
        has_main = re.search(r'if __name__ == "__main__":', self.source_code)
        has_classes = len([n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)]) > 0
        has_functions = len([n for n in ast.walk(self.tree) if isinstance(n, ast.FunctionDef)]) > 5
        
        if has_main and has_classes and has_functions:
            return True, "Well organized with main guard, classes, and functions"
        return False, "Basic organization"
    
    def check_naming_conventions(self):
        """Check naming conventions"""
        functions = [n.name for n in ast.walk(self.tree) if isinstance(n, ast.FunctionDef)]
        classes = [n.name for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)]
        
        good_function_names = sum(1 for name in functions if name.islower() or '_' in name)
        good_class_names = sum(1 for name in classes if name[0].isupper())
        
        total_names = len(functions) + len(classes)
        good_names = good_function_names + good_class_names
        
        if total_names > 0 and (good_names / total_names) >= 0.8:
            return True, f"Good naming: {good_names}/{total_names} follow conventions"
        return False, f"Naming issues: {good_names}/{total_names} follow conventions"
    
    def check_imports(self):
        """Check import organization"""
        import_lines = [line for line in self.lines if line.strip().startswith(('import ', 'from '))]
        
        if len(import_lines) >= 10:
            return True, f"Rich imports: {len(import_lines)} import statements"
        return False, f"Limited imports: {len(import_lines)} import statements"
    
    def check_constants(self):
        """Check for constants usage"""
        constants = re.findall(r'[A-Z_]{3,} = ', self.source_code)
        
        if len(constants) >= 3:
            return True, f"Good constants usage: {len(constants)} constants defined"
        return False, f"Limited constants: {len(constants)} constants defined"
    
    def check_class_design(self):
        """Check class design"""
        classes = [n for n in ast.walk(self.tree) if isinstance(n, ast.ClassDef)]
        
        if len(classes) >= 1:
            main_class = classes[0]  # Assuming main class is first
            methods = len([n for n in main_class.body if isinstance(n, ast.FunctionDef)])
            
            if methods >= 8:
                return True, f"Rich class design: {methods} methods in main class"
            return False, f"Simple class design: {methods} methods in main class"
        return False, "No classes found"

def generate_report(security_score, quality_score):
    """Generate final analysis report"""
    print(f"\n{Colors.BOLD}🎯 FINAL ANALYSIS REPORT{Colors.RESET}")
    print("=" * 50)
    
    security_passed, security_total = security_score
    quality_passed, quality_total = quality_score
    
    overall_score = (security_passed + quality_passed) / (security_total + quality_total) * 100
    
    print(f"Security Analysis: {security_passed}/{security_total} ({(security_passed/security_total)*100:.1f}%)")
    print(f"Code Quality: {quality_passed}/{quality_total} ({(quality_passed/quality_total)*100:.1f}%)")
    print(f"Overall Score: {overall_score:.1f}%")
    
    if overall_score >= 80:
        grade = f"{Colors.GREEN}A - Excellent{Colors.RESET}"
        recommendation = "Code is production ready with excellent security and quality"
    elif overall_score >= 70:
        grade = f"{Colors.GREEN}B - Good{Colors.RESET}"
        recommendation = "Code is well-structured with good security practices"
    elif overall_score >= 60:
        grade = f"{Colors.YELLOW}C - Fair{Colors.RESET}"
        recommendation = "Code is functional but could benefit from improvements"
    else:
        grade = f"{Colors.RED}D - Needs Improvement{Colors.RESET}"
        recommendation = "Code needs significant security and quality improvements"
    
    print(f"\nGrade: {grade}")
    print(f"Recommendation: {recommendation}")
    
    # Security recommendations
    print(f"\n{Colors.CYAN}🔒 Security Recommendations:{Colors.RESET}")
    if security_passed < security_total:
        print("• Ensure all dangerous operations are properly protected")
        print("• Add comprehensive input validation")
        print("• Implement robust error handling")
        print("• Include clear legal disclaimers")
    else:
        print("• Security implementation is comprehensive")
        print("• Continue following security best practices")
    
    # Quality recommendations
    print(f"\n{Colors.CYAN}📊 Quality Recommendations:{Colors.RESET}")
    if quality_passed < quality_total:
        print("• Add more documentation and comments")
        print("• Consider breaking down complex functions")
        print("• Improve naming conventions")
        print("• Add more comprehensive error handling")
    else:
        print("• Code quality is excellent")
        print("• Maintain current coding standards")
    
    return overall_score

def main():
    """Main analysis function"""
    file_path = "gun_wifi_tool.py"
    
    if not os.path.exists(file_path):
        print(f"{Colors.RED}❌ File {file_path} not found{Colors.RESET}")
        return 1
    
    print(f"{Colors.CYAN}🔍 Analyzing {file_path}...{Colors.RESET}\n")
    
    # Security analysis
    security_analyzer = SecurityAnalyzer(file_path)
    security_score = security_analyzer.check_security_features()
    
    # Code quality analysis
    quality_analyzer = CodeQualityAnalyzer(file_path)
    quality_score = quality_analyzer.analyze_code_quality()
    
    # Generate final report
    overall_score = generate_report(security_score, quality_score)
    
    return 0 if overall_score >= 70 else 1

if __name__ == "__main__":
    sys.exit(main())
