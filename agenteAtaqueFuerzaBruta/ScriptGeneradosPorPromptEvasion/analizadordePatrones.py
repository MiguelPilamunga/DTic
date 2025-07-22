import pandas as pd
import re
from collections import Counter
import logging
from typing import List, Dict, Set
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PasswordPatternAnalyzer:
    def __init__(self):
        self.files = {
            'rockyou': 'rockyou.txt',
            'chat': 'chat_generate.txt',
            'claude': 'claude_generados.txt',
            'copilot': 'copilot_generator.txt'
        }
        self.patterns = {}
        self.common_patterns = {
            'numeric_suffix': r'.*\d+$',
            'numeric_prefix': r'^\d+.*',
            'special_suffix': r'.*[!@#$%^&*()_+\-=\[\]{};:,.<>?]$',
            'special_prefix': r'^[!@#$%^&*()_+\-=\[\]{};:,.<>?].*',
            'leet_speak': r'.*[4@3310$]+.*',  # Patrones de leetspeak (a=4, e=3, i=1, etc.)
            'keyboard_pattern': r'.*(qwerty|asdf|zxcv).*',
            'repeated_chars': r'(.)\1{2,}',
            'year_pattern': r'.*(19|20)\d{2}.*',
            'common_words': r'.*(password|admin|login|welcome|123456|qwerty).*'
        }

    def load_and_analyze_file(self, filename: str) -> Dict:
        """Carga y analiza un archivo de contraseñas."""
        try:
            with open(filename, 'r', encoding='latin-1') as f:
                passwords = [line.strip() for line in f if line.strip()]

            analysis = {
                'total_passwords': len(passwords),
                'pattern_counts': self._analyze_patterns(passwords),
                'length_stats': self._analyze_length(passwords),
                'char_stats': self._analyze_char_types(passwords),
                'common_segments': self._find_common_segments(passwords)
            }
            return analysis
        except Exception as e:
            logger.error(f"Error al analizar {filename}: {str(e)}")
            return {}

    def _analyze_patterns(self, passwords: List[str]) -> Dict:
        """Analiza los patrones en las contraseñas."""
        pattern_counts = {name: 0 for name in self.common_patterns}

        for pwd in passwords:
            for pattern_name, pattern in self.common_patterns.items():
                if re.search(pattern, pwd):
                    pattern_counts[pattern_name] += 1

        return {k: v/len(passwords)*100 for k, v in pattern_counts.items()}

    def _analyze_length(self, passwords: List[str]) -> Dict:
        """Analiza las estadísticas de longitud."""
        lengths = [len(pwd) for pwd in passwords]
        return {
            'mean': sum(lengths)/len(lengths),
            'most_common': Counter(lengths).most_common(3)
        }

    def _analyze_char_types(self, passwords: List[str]) -> Dict:
        """Analiza los tipos de caracteres utilizados."""
        stats = {
            'lowercase': 0,
            'uppercase': 0,
            'digits': 0,
            'special': 0
        }

        total = len(passwords)
        for pwd in passwords:
            if re.search(r'[a-z]', pwd): stats['lowercase'] += 1
            if re.search(r'[A-Z]', pwd): stats['uppercase'] += 1
            if re.search(r'[0-9]', pwd): stats['digits'] += 1
            if re.search(r'[^a-zA-Z0-9]', pwd): stats['special'] += 1

        return {k: v/total*100 for k, v in stats.items()}

    def _find_common_segments(self, passwords: List[str], min_length: int = 3) -> List[tuple]:
        """Encuentra segmentos comunes en las contraseñas."""
        segments = Counter()

        for pwd in passwords:
            for i in range(len(pwd)-min_length+1):
                for j in range(i+min_length, min(i+8, len(pwd)+1)):
                    segment = pwd[i:j]
                    segments[segment] += 1

        return segments.most_common(10)

    def compare_all_files(self) -> Dict:
        """Compara los patrones entre todos los archivos."""
        all_analysis = {}

        for source, filename in self.files.items():
            all_analysis[source] = self.load_and_analyze_file(filename)

        comparison = {
            'pattern_similarities': self._compare_patterns(all_analysis),
            'length_comparison': self._compare_lengths(all_analysis),
            'char_type_comparison': self._compare_char_types(all_analysis),
            'unique_characteristics': self._find_unique_characteristics(all_analysis)
        }

        return comparison

    def _compare_patterns(self, analyses: Dict) -> Dict:
        """Compara los patrones entre diferentes fuentes."""
        pattern_similarities = {}

        for pattern in self.common_patterns:
            pattern_similarities[pattern] = {
                source: analysis.get('pattern_counts', {}).get(pattern, 0)
                for source, analysis in analyses.items()
            }

        return pattern_similarities

    def _compare_lengths(self, analyses: Dict) -> Dict:
        """Compara las estadísticas de longitud entre fuentes."""
        return {
            source: analysis.get('length_stats', {})
            for source, analysis in analyses.items()
        }

    def _compare_char_types(self, analyses: Dict) -> Dict:
        """Compara los tipos de caracteres entre fuentes."""
        return {
            source: analysis.get('char_stats', {})
            for source, analysis in analyses.items()
        }

    def _find_unique_characteristics(self, analyses: Dict) -> Dict:
        """Identifica características únicas de cada fuente."""
        unique_chars = {}

        for source, analysis in analyses.items():
            patterns = analysis.get('pattern_counts', {})
            char_stats = analysis.get('char_stats', {})

            unique_chars[source] = {
                'distinctive_patterns': [
                    pattern for pattern, value in patterns.items()
                    if value > sum(a.get('pattern_counts', {}).get(pattern, 0)
                                   for s, a in analyses.items() if s != source)/3
                ],
                'distinctive_chars': {
                    char_type: value for char_type, value in char_stats.items()
                    if value > sum(a.get('char_stats', {}).get(char_type, 0)
                                   for s, a in analyses.items() if s != source)/3
                }
            }

        return unique_chars

def main():
    analyzer = PasswordPatternAnalyzer()
    comparison = analyzer.compare_all_files()

    # Mostrar resultados
    logger.info("\n=== ANÁLISIS COMPARATIVO DE PATRONES ===")

    # Patrones comunes
    logger.info("\nPatrones comunes en todos los archivos:")
    for pattern, values in comparison['pattern_similarities'].items():
        logger.info(f"\n{pattern}:")
        for source, percentage in values.items():
            logger.info(f"  {source}: {percentage:.1f}%")

    # Longitudes
    logger.info("\nComparación de longitudes:")
    for source, stats in comparison['length_comparison'].items():
        logger.info(f"\n{source}:")
        logger.info(f"  Media: {stats.get('mean', 0):.1f}")
        logger.info(f"  Longitudes más comunes: {stats.get('most_common', [])}")

    # Tipos de caracteres
    logger.info("\nComparación de tipos de caracteres:")
    for source, stats in comparison['char_type_comparison'].items():
        logger.info(f"\n{source}:")
        for char_type, percentage in stats.items():
            logger.info(f"  {char_type}: {percentage:.1f}%")

    # Características únicas
    logger.info("\nCaracterísticas distintivas:")
    for source, unique in comparison['unique_characteristics'].items():
        logger.info(f"\n{source}:")
        logger.info(f"  Patrones distintivos: {unique['distinctive_patterns']}")
        logger.info(f"  Caracteres distintivos: {unique['distinctive_chars']}")

if __name__ == "__main__":
    main()