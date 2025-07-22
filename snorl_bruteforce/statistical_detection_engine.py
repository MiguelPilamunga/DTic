#!/usr/bin/env python3
"""
Motor de Detección Estadística Basado en Resultados
Analiza patrones estadísticos específicos de nuestro sistema integrado
Educational/Research purposes only
"""

import sqlite3
import numpy as np
import time
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import defaultdict
import re

@dataclass
class ConnectionEvent:
    """Evento de conexión para análisis"""
    timestamp: float
    src_ip: str
    dst_ip: str
    dst_port: int
    username: str = ""
    password: str = ""
    success: bool = False
    protocol: str = "ssh"

class StatisticalPatternDetector:
    """Detector de patrones estadísticos basado en nuestros resultados"""
    
    def __init__(self, db_path: str = "detection_analysis.sqlite"):
        self.db_path = db_path
        self.init_database()
        
        # Patrones específicos de nuestro sistema
        self.known_patterns = {
            'ecuadorian_substitutions': r'[\$@301][a-zA-Z0-9\$@301]*[@\*#!%&+=]{1,3}$',
            'cultural_references': r'(batman|peluchin|halamadrid|barcelona|real|ecuador|quito|cuenca|liga|condor)',
            'name_year_pattern': r'[a-zA-Z]+(19[8-9][0-9]|20[0-1][0-9])[@\*#!]{0,2}$',
            'institution_pattern': r'(luis|miguel|andrea|diego)(puce|uce|usfq|epn|utn|utpl)',
            'multiple_symbols': r'[a-zA-Z0-9]+[@\*#!%&+=]{2,4}$',
            'specific_sequences': r'[a-zA-Z]+(123|321|456|789|1998|1996|2024)[@\*#!]{0,2}$'
        }
        
        # Umbrales basados en nuestro análisis
        self.thresholds = {
            'ultra_stealth_min_interval': 300,  # 5 minutos mínimo
            'ultra_stealth_max_interval': 1800,  # 30 minutos máximo
            'lognormal_detection_threshold': 0.85,  # Nivel de confianza
            'cultural_pattern_threshold': 0.7,
            'timing_regularity_threshold': 0.8
        }
        
        self.detection_stats = {
            'total_connections_analyzed': 0,
            'stealth_attacks_detected': 0,
            'cultural_patterns_detected': 0,
            'lognormal_distributions_detected': 0,
            'false_positive_rate': 0.0
        }
        
    def init_database(self):
        """Inicializar base de datos de detección"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS connection_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                src_ip TEXT,
                dst_ip TEXT,
                dst_port INTEGER,
                username TEXT,
                password TEXT,
                success BOOLEAN,
                protocol TEXT,
                detected_patterns TEXT,
                risk_score REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS detection_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                src_ip TEXT,
                alert_type TEXT,
                confidence_level REAL,
                evidence TEXT,
                mitigated BOOLEAN DEFAULT FALSE
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def analyze_connection_event(self, event: ConnectionEvent) -> Dict:
        """Analizar evento de conexión individual"""
        analysis = {
            'timestamp': event.timestamp,
            'src_ip': event.src_ip,
            'detected_patterns': [],
            'risk_score': 0.0,
            'alerts': []
        }
        
        # 1. Análisis de patrones de contraseña
        if event.password:
            pattern_analysis = self.analyze_password_patterns(event.password)
            analysis['detected_patterns'].extend(pattern_analysis['patterns'])
            analysis['risk_score'] += pattern_analysis['risk_score']
            
        # 2. Análisis de timing (requiere historial)
        timing_analysis = self.analyze_timing_patterns(event.src_ip, event.timestamp)
        if timing_analysis['suspicious']:
            analysis['detected_patterns'].append('suspicious_timing')
            analysis['risk_score'] += timing_analysis['risk_score']
            
        # 3. Análisis de distribución estadística
        distribution_analysis = self.analyze_statistical_distribution(event.src_ip)
        if distribution_analysis['is_lognormal']:
            analysis['detected_patterns'].append('lognormal_distribution')
            analysis['risk_score'] += 30
            analysis['alerts'].append({
                'type': 'ULTRA_STEALTH_ATTACK',
                'confidence': distribution_analysis['confidence'],
                'evidence': f"Lognormal distribution detected with confidence {distribution_analysis['confidence']:.2f}"
            })
            
        # Almacenar en base de datos
        self.store_analysis(event, analysis)
        
        return analysis
        
    def analyze_password_patterns(self, password: str) -> Dict:
        """Analizar patrones específicos de contraseña basados en nuestros resultados"""
        analysis = {
            'patterns': [],
            'risk_score': 0
        }
        
        # Verificar patrones específicos de nuestro sistema
        for pattern_name, pattern_regex in self.known_patterns.items():
            if re.search(pattern_regex, password, re.IGNORECASE):
                analysis['patterns'].append(pattern_name)
                
                # Puntuaciones específicas basadas en nuestros resultados
                if pattern_name == 'ecuadorian_substitutions':
                    analysis['risk_score'] += 25  # Alto riesgo - patrón muy específico
                elif pattern_name == 'cultural_references':
                    analysis['risk_score'] += 20  # Contexto cultural ecuatoriano
                elif pattern_name == 'name_year_pattern':
                    analysis['risk_score'] += 15  # Patrón nombre+año común
                elif pattern_name == 'institution_pattern':
                    analysis['risk_score'] += 30  # Muy específico de nuestro dataset
                elif pattern_name == 'multiple_symbols':
                    analysis['risk_score'] += 10  # Patrón común pero relevante
                elif pattern_name == 'specific_sequences':
                    analysis['risk_score'] += 12  # Secuencias específicas
                    
        # Verificar patrones exactos de nuestro wordlist
        high_risk_passwords = [
            '$13rr@', '@nd3$', '3pn123', 'qu1t0', 'puc3123', 'c0nd0r',
            'cu3nc@', 'lu1$96', 'm@x123', 'di3g0', 'r3@l', 'batman123',
            'andrea96', 'luis1996', 'miguel@', 'diego05'
        ]
        
        if password.lower() in [p.lower() for p in high_risk_passwords]:
            analysis['patterns'].append('exact_wordlist_match')
            analysis['risk_score'] += 50  # Máximo riesgo
            
        return analysis
        
    def analyze_timing_patterns(self, src_ip: str, current_timestamp: float) -> Dict:
        """Analizar patrones de timing ultra-stealth"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obtener últimas 10 conexiones de la misma IP
        cursor.execute('''
            SELECT timestamp FROM connection_events 
            WHERE src_ip = ? 
            ORDER BY timestamp DESC 
            LIMIT 10
        ''', (src_ip,))
        
        timestamps = [row[0] for row in cursor.fetchall()]
        timestamps.append(current_timestamp)
        timestamps.sort()
        
        conn.close()
        
        analysis = {
            'suspicious': False,
            'risk_score': 0,
            'intervals': [],
            'characteristics': []
        }
        
        if len(timestamps) < 3:
            return analysis
            
        # Calcular intervalos
        intervals = []
        for i in range(1, len(timestamps)):
            interval = timestamps[i] - timestamps[i-1]
            intervals.append(interval)
            
        analysis['intervals'] = intervals
        
        if not intervals:
            return analysis
            
        # Análisis específico para ultra-stealth (5-30 minutos)
        ultra_stealth_intervals = [i for i in intervals if 300 <= i <= 1800]
        
        if len(ultra_stealth_intervals) >= 3:
            analysis['suspicious'] = True
            analysis['risk_score'] += 25
            analysis['characteristics'].append('ultra_stealth_timing')
            
        # Análisis de regularidad (característica de nuestro sistema)
        if len(intervals) >= 5:
            mean_interval = np.mean(intervals)
            std_interval = np.std(intervals)
            regularity_score = 1 - (std_interval / mean_interval) if mean_interval > 0 else 0
            
            if regularity_score > self.thresholds['timing_regularity_threshold']:
                analysis['suspicious'] = True
                analysis['risk_score'] += 20
                analysis['characteristics'].append('suspicious_regularity')
                
        return analysis
        
    def analyze_statistical_distribution(self, src_ip: str) -> Dict:
        """Detectar distribución lognormal específica de nuestro sistema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Obtener intervalos históricos
        cursor.execute('''
            SELECT timestamp FROM connection_events 
            WHERE src_ip = ? 
            ORDER BY timestamp 
            LIMIT 20
        ''', (src_ip,))
        
        timestamps = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        analysis = {
            'is_lognormal': False,
            'confidence': 0.0,
            'parameters': None
        }
        
        if len(timestamps) < 8:  # Necesitamos suficientes muestras
            return analysis
            
        # Calcular intervalos
        intervals = []
        for i in range(1, len(timestamps)):
            interval = timestamps[i] - timestamps[i-1]
            if interval > 0:  # Evitar intervalos cero
                intervals.append(interval)
                
        if len(intervals) < 5:
            return analysis
            
        try:
            # Análisis lognormal
            log_intervals = np.log(intervals)
            
            # Parámetros de distribución lognormal de nuestro sistema
            # Base interval: 8-25 minutos = 480-1500 segundos
            expected_mu = np.log(900)  # Media logarítmica esperada
            expected_sigma = 0.4  # Desviación estándar logarítmica esperada
            
            # Calcular parámetros observados
            observed_mu = np.mean(log_intervals)
            observed_sigma = np.std(log_intervals)
            
            # Calcular similitud con nuestro patrón
            mu_similarity = 1 - abs(observed_mu - expected_mu) / expected_mu
            sigma_similarity = 1 - abs(observed_sigma - expected_sigma) / expected_sigma
            
            overall_similarity = (mu_similarity + sigma_similarity) / 2
            
            # Si la similitud es alta, es probable que sea nuestro sistema
            if overall_similarity > self.thresholds['lognormal_detection_threshold']:
                analysis['is_lognormal'] = True
                analysis['confidence'] = overall_similarity
                analysis['parameters'] = {
                    'mu': observed_mu,
                    'sigma': observed_sigma,
                    'similarity_to_attack': overall_similarity
                }
                
        except Exception as e:
            # En caso de error en cálculos estadísticos
            pass
            
        return analysis
        
    def store_analysis(self, event: ConnectionEvent, analysis: Dict):
        """Almacenar análisis en base de datos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO connection_events 
            (timestamp, src_ip, dst_ip, dst_port, username, password, success, protocol, detected_patterns, risk_score)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event.timestamp,
            event.src_ip,
            event.dst_ip,
            event.dst_port,
            event.username,
            event.password,
            event.success,
            event.protocol,
            json.dumps(analysis['detected_patterns']),
            analysis['risk_score']
        ))
        
        # Generar alertas de alto riesgo
        if analysis['risk_score'] >= 40:  # Umbral alto
            for alert in analysis.get('alerts', []):
                cursor.execute('''
                    INSERT INTO detection_alerts
                    (timestamp, src_ip, alert_type, confidence_level, evidence)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    event.timestamp,
                    event.src_ip,
                    alert['type'],
                    alert['confidence'],
                    alert['evidence']
                ))
                
        conn.commit()
        conn.close()
        
        # Actualizar estadísticas
        self.update_detection_stats(analysis)
        
    def update_detection_stats(self, analysis: Dict):
        """Actualizar estadísticas de detección"""
        self.detection_stats['total_connections_analyzed'] += 1
        
        if 'lognormal_distribution' in analysis['detected_patterns']:
            self.detection_stats['lognormal_distributions_detected'] += 1
            
        if 'cultural_references' in analysis['detected_patterns']:
            self.detection_stats['cultural_patterns_detected'] += 1
            
        if analysis['risk_score'] >= 40:
            self.detection_stats['stealth_attacks_detected'] += 1
            
    def generate_detection_report(self) -> Dict:
        """Generar reporte de detección"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Estadísticas generales
        cursor.execute('SELECT COUNT(*) FROM connection_events')
        total_events = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM detection_alerts WHERE mitigated = FALSE')
        active_alerts = cursor.fetchone()[0]
        
        cursor.execute('''
            SELECT src_ip, COUNT(*) as count, AVG(risk_score) as avg_risk
            FROM connection_events 
            GROUP BY src_ip 
            HAVING COUNT(*) >= 5 
            ORDER BY avg_risk DESC 
            LIMIT 10
        ''')
        high_risk_sources = cursor.fetchall()
        
        conn.close()
        
        report = {
            'generation_time': datetime.now().isoformat(),
            'summary': {
                'total_events_analyzed': total_events,
                'active_alerts': active_alerts,
                'detection_effectiveness': f"{(self.detection_stats['stealth_attacks_detected'] / max(1, self.detection_stats['total_connections_analyzed'])) * 100:.1f}%"
            },
            'pattern_detection': {
                'lognormal_attacks_detected': self.detection_stats['lognormal_distributions_detected'],
                'cultural_patterns_detected': self.detection_stats['cultural_patterns_detected'],
                'total_stealth_attacks': self.detection_stats['stealth_attacks_detected']
            },
            'high_risk_sources': [
                {
                    'ip': ip,
                    'connection_count': count,
                    'average_risk_score': round(avg_risk, 2)
                } for ip, count, avg_risk in high_risk_sources
            ],
            'recommendations': [
                'Monitor IPs with consistent lognormal timing patterns',
                'Implement additional controls for Ecuadorian cultural password patterns',
                'Deploy automated response for risk scores > 40',
                'Regular tuning of detection thresholds based on environment'
            ]
        }
        
        return report
        
    def print_detection_summary(self):
        """Imprimir resumen de detección"""
        print("\n" + "="*80)
        print("🛡️  MOTOR DE DETECCIÓN ESTADÍSTICA - RESUMEN")
        print("="*80)
        
        print(f"📊 Conexiones analizadas: {self.detection_stats['total_connections_analyzed']}")
        print(f"🎯 Ataques stealth detectados: {self.detection_stats['stealth_attacks_detected']}")
        print(f"🇪🇨 Patrones culturales detectados: {self.detection_stats['cultural_patterns_detected']}")
        print(f"📈 Distribuciones lognormales detectadas: {self.detection_stats['lognormal_distributions_detected']}")
        
        if self.detection_stats['total_connections_analyzed'] > 0:
            effectiveness = (self.detection_stats['stealth_attacks_detected'] / 
                           self.detection_stats['total_connections_analyzed']) * 100
            print(f"✅ Efectividad de detección: {effectiveness:.1f}%")
            
        print("\n📋 PATRONES DETECTABLES:")
        for pattern_name in self.known_patterns.keys():
            print(f"   • {pattern_name}")

def main():
    """Demostración del motor de detección"""
    detector = StatisticalPatternDetector()
    
    print("🛡️  MOTOR DE DETECCIÓN ESTADÍSTICA BASADO EN RESULTADOS")
    print("Diseñado específicamente para detectar nuestro sistema integrado")
    print("="*70)
    
    # Simular eventos de conexión basados en nuestros patrones
    test_events = [
        ConnectionEvent(time.time() - 1800, "172.18.0.1", "172.18.0.2", 22, "root", "luis1996@", False),
        ConnectionEvent(time.time() - 1200, "172.18.0.1", "172.18.0.2", 22, "admin", "$13rr@", False),
        ConnectionEvent(time.time() - 600, "172.18.0.1", "172.18.0.2", 22, "root", "@nd3$", False),
        ConnectionEvent(time.time() - 300, "172.18.0.1", "172.18.0.2", 22, "root", "batman123", True),
    ]
    
    print("🔍 Analizando eventos de prueba...")
    for event in test_events:
        analysis = detector.analyze_connection_event(event)
        print(f"\n📅 {datetime.fromtimestamp(event.timestamp).strftime('%H:%M:%S')}")
        print(f"🎯 IP: {event.src_ip} → Password: {event.password}")
        print(f"⚠️  Riesgo: {analysis['risk_score']} | Patrones: {analysis['detected_patterns']}")
        
    # Generar reporte
    report = detector.generate_detection_report()
    print(f"\n📊 REPORTE DE EFECTIVIDAD:")
    print(f"   • Eventos analizados: {report['summary']['total_events_analyzed']}")
    print(f"   • Alertas activas: {report['summary']['active_alerts']}")
    print(f"   • Efectividad: {report['summary']['detection_effectiveness']}")
    
    detector.print_detection_summary()

if __name__ == "__main__":
    main()