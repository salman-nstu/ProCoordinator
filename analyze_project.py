import os
import re
from pathlib import Path
from collections import defaultdict
import json
from datetime import datetime

class ProjectAnalyzer:
    """Analyze Java project for code metrics"""
    
    def __init__(self, project_path):
        self.project_path = Path(project_path)
        self.java_files = []
        self.metrics = defaultdict(int)
        self.operators = defaultdict(int)
        self.operands = defaultdict(int)
        self.file_details = []
        self.packages = set()
        self.classes = []
        self.interfaces = []
        self.methods = []
        self.design_patterns = defaultdict(int)
        
    def find_java_files(self):
        """Find all Java files in the project"""
        for root, dirs, files in os.walk(self.project_path):
            # Skip bin and output directories
            dirs[:] = [d for d in dirs if d not in ['bin', 'output', '.git', '__pycache__']]
            
            for file in files:
                if file.endswith('.java'):
                    self.java_files.append(os.path.join(root, file))
    
    def count_lines(self, content):
        """Count different types of lines"""
        lines = content.split('\n')
        total_lines = len(lines)
        blank_lines = sum(1 for line in lines if line.strip() == '')
        
        return total_lines, blank_lines, lines
    
    def count_comments(self, lines):
        """Count single-line and multi-line comments"""
        single_line_comments = 0
        multi_line_comments = 0
        in_multiline = False
        commented_lines = 0
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Check for multi-line comments
            if '/*' in line:
                in_multiline = True
                multi_line_comments += 1
                commented_lines += 1
            
            if in_multiline and '*/' in line:
                in_multiline = False
                if '/*' not in line:  # Not a same-line comment
                    multi_line_comments += 1
                    commented_lines += 1
                i += 1
                continue
            
            # If in multiline, count this line
            if in_multiline:
                commented_lines += 1
                i += 1
                continue
            
            # Check for single-line comments
            if line.startswith('//'):
                single_line_comments += 1
                commented_lines += 1
            
            i += 1
        
        return single_line_comments, multi_line_comments, commented_lines
    
    def extract_operators(self, content):
        """Extract operators from code"""
        # Remove comments and strings first
        content = self._remove_comments_and_strings(content)
        
        # Java operators
        operators_pattern = r'[\+\-\*/%=<>!&|^~?:]|==|!=|<=|>=|&&|\|\||<<|>>|>>>|\+\+|--|->|\*=|/=|%=|\+=|-='
        found_operators = re.findall(operators_pattern, content)
        
        for op in found_operators:
            self.operators[op] += 1
            self.metrics['total_operators'] += 1
    
    def extract_operands(self, content):
        """Extract operands from code"""
        # Remove comments and strings
        content = self._remove_comments_and_strings(content)
        
        # Extract identifiers (variable names, method names, class names)
        operands_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        found_operands = re.findall(operands_pattern, content)
        
        # Filter out Java keywords
        java_keywords = {
            'public', 'private', 'protected', 'static', 'final', 'abstract',
            'class', 'interface', 'enum', 'extends', 'implements', 'new',
            'if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break',
            'continue', 'return', 'void', 'int', 'long', 'double', 'float',
            'boolean', 'char', 'byte', 'short', 'String', 'Object', 'true',
            'false', 'null', 'this', 'super', 'try', 'catch', 'finally',
            'throw', 'throws', 'synchronized', 'volatile', 'transient',
            'import', 'package', 'instanceof', 'default'
        }
        
        for operand in found_operands:
            if operand not in java_keywords:
                self.operands[operand] += 1
                self.metrics['total_operands'] += 1
    
    def _remove_comments_and_strings(self, content):
        """Remove comments and string literals"""
        # Remove multi-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove single-line comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        # Remove string literals
        content = re.sub(r'"(?:\\.|[^"\\])*"', '', content)
        # Remove character literals
        content = re.sub(r"'(?:\\.|[^'\\])*'", '', content)
        
        return content
    
    def count_executable_lines(self, lines):
        """Count executable lines of code (code lines excluding braces and declarations)"""
        eloc = 0
        for line in lines:
            stripped = line.strip()
            # Skip empty lines, comment lines, and lines with only braces
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and \
               stripped not in ['{', '}', '{', '};', ''] and \
               not re.match(r'^[{}]*$', stripped):
                eloc += 1
        return eloc
    
    def extract_structure(self, content, filepath):
        """Extract package, class, interface, and method information"""
        # Extract package
        package_match = re.search(r'package\s+([\w.]+);', content)
        if package_match:
            self.packages.add(package_match.group(1))
        
        # Extract classes
        class_matches = re.finditer(r'(?:public\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)', content)
        for match in class_matches:
            class_name = match.group(1)
            self.classes.append({
                'name': class_name,
                'file': filepath,
                'methods': 0,
                'char_count': 0
            })
        
        # Extract interfaces
        interface_matches = re.finditer(r'(?:public\s+)?interface\s+(\w+)', content)
        for match in interface_matches:
            self.interfaces.append({
                'name': match.group(1),
                'file': filepath
            })
        
        # Extract methods
        method_matches = re.finditer(
            r'(?:public|private|protected)?\s+(?:static\s+)?(?:synchronized\s+)?(?:final\s+)?'
            r'(?:\w+(?:<[\w,\s]*>)?)\s+(\w+)\s*\([^)]*\)',
            content
        )
        for match in method_matches:
            method_name = match.group(1)
            if method_name not in ['if', 'for', 'while', 'catch', 'switch']:
                self.methods.append({
                    'name': method_name,
                    'file': filepath
                })
                if self.classes:
                    self.classes[-1]['methods'] += 1
    
    def detect_design_patterns(self, content):
        """Detect common design patterns"""
        patterns = {
            'Singleton': r'(?:private\s+static.*?instance|getInstance|INSTANCE)',
            'Factory': r'(?:create[A-Z]\w*|newInstance)',
            'Observer': r'(?:addListener|removeListener|notifyListeners|notify)',
            'Strategy': r'(?:setStrategy|executeStrategy)',
            'Decorator': r'(?:public\s+\w+\s+\w+\([^)]*\)\s*\{[^}]*super)',
            'Adapter': r'(?:implements.*implements|extends.*implements)',
            'Builder': r'(?:\.with\w+\(|\.build\(\))',
            'Template Method': r'(?:protected\s+abstract.*public.*\{[^}]*)',
        }
        
        for pattern_name, pattern_regex in patterns.items():
            if re.search(pattern_regex, content, re.IGNORECASE):
                self.design_patterns[pattern_name] += 1
    
    def analyze_file(self, filepath):
        """Analyze a single Java file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            total_lines, blank_lines, lines = self.count_lines(content)
            single_comments, multi_comments, comment_lines = self.count_comments(lines)
            
            code_lines = total_lines - blank_lines - comment_lines
            eloc = self.count_executable_lines(lines)
            
            # Extract operators and operands
            self.extract_operators(content)
            self.extract_operands(content)
            
            # Extract structure information
            self.extract_structure(content, filepath)
            
            # Detect design patterns
            self.detect_design_patterns(content)
            
            # Calculate storage metrics
            char_count = len(content)
            byte_count = len(content.encode('utf-8'))
            
            # Update metrics
            self.metrics['total_files'] += 1
            self.metrics['total_lines'] += total_lines
            self.metrics['blank_lines'] += blank_lines
            self.metrics['comment_lines'] += comment_lines
            self.metrics['code_lines'] += code_lines
            self.metrics['single_line_comments'] += single_comments
            self.metrics['multi_line_comments'] += multi_comments
            self.metrics['executable_lines'] += eloc
            self.metrics['total_characters'] += char_count
            self.metrics['total_bytes'] += byte_count
            
            # Store file details
            file_rel_path = os.path.relpath(filepath, self.project_path)
            self.file_details.append({
                'file': file_rel_path,
                'total_lines': total_lines,
                'blank_lines': blank_lines,
                'comment_lines': comment_lines,
                'code_lines': code_lines,
                'executable_lines': eloc,
                'single_comments': single_comments,
                'multi_comments': multi_comments,
                'characters': char_count,
                'bytes': byte_count
            })
            
        except Exception as e:
            print(f"Error analyzing {filepath}: {e}")
    
    def calculate_halstead_metrics(self):
        """Calculate Halstead metrics"""
        n1 = len(self.operators)  # Number of distinct operators
        n2 = len(self.operands)   # Number of distinct operands
        N1 = self.metrics['total_operators']  # Total operators
        N2 = self.metrics['total_operands']   # Total operands
        
        if n1 > 0 and n2 > 0 and N1 > 0 and N2 > 0:
            # Program length
            program_length = N1 + N2
            
            # Program vocabulary
            program_vocabulary = n1 + n2
            
            # Volume (bits)
            import math
            volume = program_length * math.log2(program_vocabulary) if program_vocabulary > 0 else 0
            
            # Difficulty
            difficulty = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
            
            # Effort
            effort = difficulty * volume
            
            # Estimated time (in hours)
            time_hours = effort / 3600 if effort > 0 else 0
            
            self.metrics['halstead_program_length'] = program_length
            self.metrics['halstead_vocabulary'] = program_vocabulary
            self.metrics['halstead_volume'] = volume
            self.metrics['halstead_difficulty'] = difficulty
            self.metrics['halstead_effort'] = effort
            self.metrics['halstead_time_hours'] = time_hours
    
    def generate_report(self):
        """Generate a comprehensive analysis report"""
        report = []
        report.append("=" * 90)
        report.append("PROJECT CODE ANALYSIS REPORT - HALSTEAD & CODE METRICS".center(90))
        report.append("=" * 90)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # ============ CODE SIZE METRICS ============
        report.append("\n" + "=" * 90)
        report.append("1. DETERMINING CODE SIZE FOR SPL-I PROJECTED".center(90))
        report.append("=" * 90)
        
        report.append("\n1.1 Lines of Code (LOC)".ljust(90))
        report.append("-" * 90)
        report.append(f"  Total Lines of Code (LOC):        {self.metrics['total_lines']:>15}")
        
        report.append("\n1.2 Commented Lines of Code (CLOC)".ljust(90))
        report.append("-" * 90)
        report.append(f"  Single-line Comments:             {self.metrics['single_line_comments']:>15}")
        report.append(f"  Multi-line Comments:              {self.metrics['multi_line_comments']:>15}")
        report.append(f"  Total Commented Lines:            {self.metrics['comment_lines']:>15}")
        
        report.append("\n1.3 Non-Commented Lines of Code (NCLOC)".ljust(90))
        report.append("-" * 90)
        ncloc = self.metrics['code_lines']
        report.append(f"  Non-Commented Lines:              {ncloc:>15}")
        
        report.append("\n1.4 Executable Lines of Code (ELOC)".ljust(90))
        report.append("-" * 90)
        report.append(f"  Executable Lines of Code:         {self.metrics['executable_lines']:>15}")
        
        report.append("\n1.5 Blank Lines of Code".ljust(90))
        report.append("-" * 90)
        report.append(f"  Blank Lines:                      {self.metrics['blank_lines']:>15}")
        
        report.append("\n1.6 Density of Comments".ljust(90))
        report.append("-" * 90)
        if self.metrics['total_lines'] > 0:
            comment_density = (self.metrics['comment_lines'] / self.metrics['total_lines']) * 100
            report.append(f"  Comment Density:                  {comment_density:>14.2f}%")
        
        report.append("\n1.7 Overall Line Statistics Breakdown".ljust(90))
        report.append("-" * 90)
        if self.metrics['total_lines'] > 0:
            code_pct = (self.metrics['code_lines'] / self.metrics['total_lines']) * 100
            comment_pct = (self.metrics['comment_lines'] / self.metrics['total_lines']) * 100
            blank_pct = (self.metrics['blank_lines'] / self.metrics['total_lines']) * 100
            
            report.append(f"  Code Lines:        {self.metrics['code_lines']:>10}  ({code_pct:>6.2f}%)")
            report.append(f"  Comment Lines:     {self.metrics['comment_lines']:>10}  ({comment_pct:>6.2f}%)")
            report.append(f"  Blank Lines:       {self.metrics['blank_lines']:>10}  ({blank_pct:>6.2f}%)")
            report.append(f"  Total Lines:       {self.metrics['total_lines']:>10}  (100.00%)")
        
        report.append("\n1.8 Halstead's Approach".ljust(90))
        report.append("-" * 90)
        report.append(f"  Distinct Operators (n1):          {len(self.operators):>15}")
        report.append(f"  Distinct Operands (n2):          {len(self.operands):>15}")
        report.append(f"  Total Operators (N1):            {self.metrics['total_operators']:>15}")
        report.append(f"  Total Operands (N2):             {self.metrics['total_operands']:>15}")
        
        if self.metrics.get('halstead_volume'):
            report.append(f"\n  Halstead Metrics:")
            report.append(f"    Program Length (N):           {self.metrics['halstead_program_length']:>15.0f}")
            report.append(f"    Program Vocabulary (n):       {self.metrics['halstead_vocabulary']:>15}")
            report.append(f"    Volume (bits):                {self.metrics['halstead_volume']:>15.2f}")
            report.append(f"    Difficulty:                   {self.metrics['halstead_difficulty']:>15.2f}")
            report.append(f"    Effort:                       {self.metrics['halstead_effort']:>15.2f}")
            report.append(f"    Time to Understand (hours):   {self.metrics['halstead_time_hours']:>15.2f}")
        
        report.append("\n1.9 Number of Bytes of Computer Storage".ljust(90))
        report.append("-" * 90)
        report.append(f"  Total Bytes:                      {self.metrics['total_bytes']:>15} bytes")
        report.append(f"  Total Bytes (KB):                 {self.metrics['total_bytes']/1024:>14.2f} KB")
        report.append(f"  Total Bytes (MB):                 {self.metrics['total_bytes']/1024/1024:>14.2f} MB")
        
        report.append("\n1.10 Number of Characters".ljust(90))
        report.append("-" * 90)
        report.append(f"  Total Characters:                {self.metrics['total_characters']:>15}")
        
        report.append("\n1.11 Average Number of Characters per Class".ljust(90))
        report.append("-" * 90)
        if self.classes:
            avg_chars_per_class = self.metrics['total_characters'] / len(self.classes)
            report.append(f"  Average Characters per Class:    {avg_chars_per_class:>14.2f}")
        
        # ============ DESIGN SIZE METRICS ============
        report.append("\n\n" + "=" * 90)
        report.append("2. DETERMINING DESIGN SIZE FOR SPL-I PROJECT".center(90))
        report.append("=" * 90)
        
        report.append("\n2.1 Number of Sub-packages".ljust(90))
        report.append("-" * 90)
        report.append(f"  Total Packages:                   {len(self.packages):>15}")
        if self.packages:
            for i, pkg in enumerate(sorted(self.packages), 1):
                report.append(f"    {i}. {pkg}")
        
        report.append("\n2.2 Number of Classes".ljust(90))
        report.append("-" * 90)
        report.append(f"  Total Classes:                    {len(self.classes):>15}")
        
        report.append("\n2.3 Number of Interfaces".ljust(90))
        report.append("-" * 90)
        report.append(f"  Total Interfaces:                {len(self.interfaces):>15}")
        
        report.append("\n2.4 Number of Design Patterns".ljust(90))
        report.append("-" * 90)
        total_patterns = sum(self.design_patterns.values())
        report.append(f"  Total Design Pattern Occurrences:{total_patterns:>15}")
        if self.design_patterns:
            for pattern, count in sorted(self.design_patterns.items(), key=lambda x: x[1], reverse=True):
                report.append(f"    {pattern}: {count}")
        
        report.append("\n2.5 Number of Methods".ljust(90))
        report.append("-" * 90)
        report.append(f"  Total Methods:                    {len(self.methods):>15}")
        
        report.append("\n2.6 Average Methods per Class".ljust(90))
        report.append("-" * 90)
        if self.classes:
            avg_methods = len(self.methods) / len(self.classes)
            report.append(f"  Average Methods per Class:       {avg_methods:>14.2f}")
        
        # ============ TOP OPERATORS & OPERANDS ============
        report.append("\n\n" + "=" * 90)
        report.append("3. TOP OPERATORS & OPERANDS".center(90))
        report.append("=" * 90)
        
        report.append("\n3.1 Top 15 Operators".ljust(90))
        report.append("-" * 90)
        top_operators = sorted(self.operators.items(), key=lambda x: x[1], reverse=True)[:15]
        report.append(f"  {'Operator':<30} {'Count':>10}")
        report.append("-" * 90)
        for op, count in top_operators:
            report.append(f"  {op:<30} {count:>10}")
        
        report.append("\n3.2 Top 20 Operands".ljust(90))
        report.append("-" * 90)
        top_operands = sorted(self.operands.items(), key=lambda x: x[1], reverse=True)[:20]
        report.append(f"  {'Operand':<40} {'Count':>10}")
        report.append("-" * 90)
        for operand, count in top_operands:
            report.append(f"  {operand:<40} {count:>10}")
        
        # ============ FILE BREAKDOWN ============
        report.append("\n\n" + "=" * 90)
        report.append("4. FILE-BY-FILE BREAKDOWN".center(90))
        report.append("=" * 90)
        
        report.append("\n")
        report.append(f"{'File':<50} {'Total':>8} {'Code':>8} {'Comments':>10} {'Blank':>8} {'ELOC':>8}")
        report.append("-" * 90)
        for file_info in sorted(self.file_details, key=lambda x: x['code_lines'], reverse=True):
            filename = file_info['file']
            if len(filename) > 50:
                filename = "..." + filename[-47:]
            report.append(
                f"{filename:<50} {file_info['total_lines']:>8} {file_info['code_lines']:>8} "
                f"{file_info['comment_lines']:>10} {file_info['blank_lines']:>8} {file_info['executable_lines']:>8}"
            )
        
        # ============ SUMMARY ============
        report.append("\n\n" + "=" * 90)
        report.append("5. PROJECT SUMMARY".center(90))
        report.append("=" * 90)
        
        report.append(f"\n  Total Java Files:                {self.metrics['total_files']:>15}")
        report.append(f"  Total Packages:                  {len(self.packages):>15}")
        report.append(f"  Total Classes:                   {len(self.classes):>15}")
        report.append(f"  Total Interfaces:               {len(self.interfaces):>15}")
        report.append(f"  Total Methods:                   {len(self.methods):>15}")
        report.append(f"  Total Lines of Code:             {self.metrics['total_lines']:>15}")
        report.append(f"  Total Storage (bytes):           {self.metrics['total_bytes']:>15}")
        report.append(f"  Total Characters:               {self.metrics['total_characters']:>15}")
        
        report.append("\n" + "=" * 90)
        
        return "\n".join(report)
    
    def run(self):
        """Run the analysis"""
        print("Scanning for Java files...")
        self.find_java_files()
        
        if not self.java_files:
            print("No Java files found!")
            return
        
        print(f"Found {len(self.java_files)} Java files. Analyzing...")
        
        for filepath in self.java_files:
            self.analyze_file(filepath)
        
        self.calculate_halstead_metrics()
        
        report = self.generate_report()
        print(report)
        
        # Save report to file
        output_file = self.project_path / "analysis_report.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\nReport saved to: {output_file}")
        
        # Save detailed metrics as JSON
        json_file = self.project_path / "analysis_metrics.json"
        metrics_data = {
            'timestamp': datetime.now().isoformat(),
            'project_overview': {
                'total_files': self.metrics['total_files'],
                'total_packages': len(self.packages),
                'total_classes': len(self.classes),
                'total_interfaces': len(self.interfaces),
                'total_methods': len(self.methods),
            },
            'code_size_metrics': {
                'loc': self.metrics['total_lines'],
                'cloc': self.metrics['comment_lines'],
                'ncloc': self.metrics['code_lines'],
                'eloc': self.metrics['executable_lines'],
                'blank_lines': self.metrics['blank_lines'],
                'comment_density': (self.metrics['comment_lines'] / self.metrics['total_lines'] * 100) if self.metrics['total_lines'] > 0 else 0,
                'total_bytes': self.metrics['total_bytes'],
                'total_characters': self.metrics['total_characters'],
                'avg_chars_per_class': (self.metrics['total_characters'] / len(self.classes)) if self.classes else 0,
            },
            'design_size_metrics': {
                'packages': list(self.packages),
                'classes': len(self.classes),
                'interfaces': len(self.interfaces),
                'design_patterns': dict(self.design_patterns),
                'methods': len(self.methods),
                'avg_methods_per_class': (len(self.methods) / len(self.classes)) if self.classes else 0,
            },
            'halstead_metrics': {
                'distinct_operators': len(self.operators),
                'distinct_operands': len(self.operands),
                'total_operators': self.metrics['total_operators'],
                'total_operands': self.metrics['total_operands'],
                'program_length': self.metrics.get('halstead_program_length', 0),
                'program_vocabulary': self.metrics.get('halstead_vocabulary', 0),
                'volume': self.metrics.get('halstead_volume', 0),
                'difficulty': self.metrics.get('halstead_difficulty', 0),
                'effort': self.metrics.get('halstead_effort', 0),
                'time_hours': self.metrics.get('halstead_time_hours', 0),
            },
            'top_operators': dict(sorted(self.operators.items(), key=lambda x: x[1], reverse=True)[:20]),
            'top_operands': dict(sorted(self.operands.items(), key=lambda x: x[1], reverse=True)[:20]),
            'file_details': self.file_details
        }
        
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2)
        
        print(f"Metrics saved to: {json_file}")


if __name__ == "__main__":
    # Analyze the project
    project_root = Path(__file__).parent
    analyzer = ProjectAnalyzer(project_root)
    analyzer.run()
