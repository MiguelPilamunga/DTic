import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
import time

class CognitiveState(Enum):
    """Estados cognitivos para modelar carga mental en interacción digital"""
    LOW = "bajo"
    MEDIUM = "medio"
    HIGH = "alto"

class ActionType(Enum):
    """Tipos de acciones en la interacción digital"""
    TYPING = "escritura"
    PAUSE = "pausa"
    CORRECTION = "corrección"
    NAVIGATION = "navegación"
    REFLECTION = "reflexión"

@dataclass
class UserProfile:
    """Perfil de usuario para modelado cognitivo"""
    name: str
    base_typing_speed: float  # caracteres por segundo
    cognitive_load_factor: float  # multiplicador de pausa
    error_rate: float  # probabilidad de error
    multitasking_tendency: float  # tendencia a interrupciones
    reflection_frequency: float  # frecuencia de pausas reflexivas

class InteractionPatternModel:
    """
    Modelo estadístico para representar patrones de interacción humana digital
    
    Propósito: Investigación en UX, accesibilidad y carga cognitiva
    Uso ético: Datos sintéticos para mejorar diseño de interfaces
    """
    
    def __init__(self, research_context: str = "UX_Research"):
        """
        Inicializa el modelo de patrones de interacción
        
        Args:
            research_context: Contexto de investigación para trazabilidad ética
        """
        self.research_context = research_context
        self.interaction_log = []
        self.session_start_time = None
        
        # Perfiles de usuario predefinidos para investigación cognitiva
        self.user_profiles = {
            "novato_reflexivo": UserProfile(
                name="Novato Reflexivo",
                base_typing_speed=1.2,  # chars/sec
                cognitive_load_factor=2.5,
                error_rate=0.15,
                multitasking_tendency=0.1,
                reflection_frequency=0.3
            ),
            "multitarea_interrumpido": UserProfile(
                name="Multitarea Interrumpido",
                base_typing_speed=2.8,
                cognitive_load_factor=1.8,
                error_rate=0.08,
                multitasking_tendency=0.6,
                reflection_frequency=0.15
            ),
            "experto_continuo": UserProfile(
                name="Experto Continuo",
                base_typing_speed=4.2,
                cognitive_load_factor=1.2,
                error_rate=0.03,
                multitasking_tendency=0.05,
                reflection_frequency=0.08
            )
        }
    
    def get_next_action_delay(self, cognitive_state: CognitiveState, 
                            profile: UserProfile) -> float:
        """
        Calcula el retraso entre acciones basado en carga cognitiva
        
        Modela distribuciones temporales realistas según investigación cognitiva
        """
        base_delay = 1.0 / profile.base_typing_speed
        
        # Factores de carga cognitiva según literatura científica
        cognitive_multipliers = {
            CognitiveState.LOW: 1.0,
            CognitiveState.MEDIUM: 1.5,
            CognitiveState.HIGH: 2.5
        }
        
        cognitive_factor = cognitive_multipliers[cognitive_state]
        adjusted_delay = base_delay * cognitive_factor * profile.cognitive_load_factor
        
        # Distribución lognormal para modelar variabilidad humana realista
        noise = np.random.lognormal(0, 0.3)
        
        return max(0.1, adjusted_delay * noise)
    
    def _determine_cognitive_state(self, profile: UserProfile, 
                                 action_count: int) -> CognitiveState:
        """Determina estado cognitivo basado en perfil y progreso de sesión"""
        
        # Fatiga cognitiva aumenta con el tiempo
        fatigue_factor = min(action_count / 100, 1.0)
        
        # Interrupciones según perfil
        interruption_prob = profile.multitasking_tendency * (1 + fatigue_factor)
        
        if random.random() < interruption_prob:
            return CognitiveState.HIGH
        elif random.random() < 0.3 + fatigue_factor:
            return CognitiveState.MEDIUM
        else:
            return CognitiveState.LOW
    
    def generate_typing_sequence(self, text: str, profile: UserProfile) -> List[Dict]:
        """
        Genera secuencia de escritura con patrones cognitivos realistas
        
        Incluye pausas naturales, correcciones y variabilidad temporal
        """
        sequence = []
        current_time = 0
        action_count = 0
        
        i = 0
        while i < len(text):
            char = text[i]
            action_count += 1
            
            # Determinar estado cognitivo actual
            cognitive_state = self._determine_cognitive_state(profile, action_count)
            
            # Calcular retraso para esta acción
            delay = self.get_next_action_delay(cognitive_state, profile)
            current_time += delay
            
            # Pausa reflexiva en puntuación
            if char in '.!?,' and random.random() < profile.reflection_frequency:
                sequence.append({
                    'timestamp': current_time,
                    'action_type': ActionType.REFLECTION.value,
                    'duration': delay * 2,
                    'cognitive_load': cognitive_state.value,
                    'character': char,
                    'metadata': {'reflection_point': True}
                })
                current_time += delay
            
            # Simular errores de escritura
            if random.random() < profile.error_rate:
                # Escribir carácter incorrecto
                wrong_char = chr(ord(char) + random.randint(-2, 2))
                sequence.append({
                    'timestamp': current_time,
                    'action_type': ActionType.TYPING.value,
                    'duration': delay,
                    'cognitive_load': cognitive_state.value,
                    'character': wrong_char,
                    'metadata': {'error': True}
                })
                current_time += delay * 0.5
                
                # Corrección
                sequence.append({
                    'timestamp': current_time,
                    'action_type': ActionType.CORRECTION.value,
                    'duration': delay * 1.5,
                    'cognitive_load': CognitiveState.MEDIUM.value,
                    'character': 'BACKSPACE',
                    'metadata': {'correction': True}
                })
                current_time += delay * 1.5
            
            # Escribir carácter correcto
            sequence.append({
                'timestamp': current_time,
                'action_type': ActionType.TYPING.value,
                'duration': delay,
                'cognitive_load': cognitive_state.value,
                'character': char,
                'metadata': {'position': i}
            })
            
            i += 1
        
        return sequence
    
    def simulate_session(self, profile_type: str, 
                        interaction_text: str = "Ejemplo de texto de prueba") -> Dict:
        """
        Simula una sesión completa de interacción para investigación UX
        
        Args:
            profile_type: Tipo de perfil de usuario
            interaction_text: Texto de ejemplo para análisis
            
        Returns:
            Diccionario con datos de sesión para análisis cognitivo
        """
        if profile_type not in self.user_profiles:
            raise ValueError(f"Perfil {profile_type} no disponible")
        
        profile = self.user_profiles[profile_type]
        self.session_start_time = datetime.now()
        
        # Generar secuencia de interacción
        typing_sequence = self.generate_typing_sequence(interaction_text, profile)
        
        # Compilar estadísticas de sesión
        session_data = {
            'research_context': self.research_context,
            'profile_type': profile_type,
            'session_start': self.session_start_time.isoformat(),
            'total_duration': typing_sequence[-1]['timestamp'] if typing_sequence else 0,
            'total_actions': len(typing_sequence),
            'typing_sequence': typing_sequence,
            'cognitive_analysis': self._analyze_cognitive_patterns(typing_sequence),
            'accessibility_metrics': self._calculate_accessibility_metrics(typing_sequence)
        }
        
        return session_data
    
    def _analyze_cognitive_patterns(self, sequence: List[Dict]) -> Dict:
        """Analiza patrones cognitivos para investigación UX"""
        if not sequence:
            return {}
        
        cognitive_loads = [action['cognitive_load'] for action in sequence]
        durations = [action['duration'] for action in sequence]
        
        return {
            'avg_response_time': np.mean(durations),
            'cognitive_load_distribution': {
                'bajo': cognitive_loads.count('bajo') / len(cognitive_loads),
                'medio': cognitive_loads.count('medio') / len(cognitive_loads),
                'alto': cognitive_loads.count('alto') / len(cognitive_loads)
            },
            'error_rate': len([a for a in sequence if a['metadata'].get('error')]) / len(sequence),
            'reflection_frequency': len([a for a in sequence if a['action_type'] == 'reflexión']) / len(sequence)
        }
    
    def _calculate_accessibility_metrics(self, sequence: List[Dict]) -> Dict:
        """Calcula métricas de accesibilidad para diseño adaptativo"""
        if not sequence:
            return {}
        
        high_load_actions = [a for a in sequence if a['cognitive_load'] == 'alto']
        long_pauses = [a for a in sequence if a['duration'] > 2.0]
        
        return {
            'high_cognitive_load_percentage': len(high_load_actions) / len(sequence) * 100,
            'long_pause_frequency': len(long_pauses) / len(sequence) * 100,
            'recommended_interface_adaptations': self._suggest_adaptations(sequence)
        }
    
    def _suggest_adaptations(self, sequence: List[Dict]) -> List[str]:
        """Sugiere adaptaciones de interfaz basadas en patrones observados"""
        suggestions = []
        
        error_rate = len([a for a in sequence if a['metadata'].get('error')]) / len(sequence)
        avg_cognitive_load = len([a for a in sequence if a['cognitive_load'] == 'alto']) / len(sequence)
        
        if error_rate > 0.1:
            suggestions.append("Implementar autocompletado inteligente")
        if avg_cognitive_load > 0.3:
            suggestions.append("Reducir elementos distractores en interfaz")
            suggestions.append("Aumentar tiempo de respuesta esperado")
        
        return suggestions
    
    def log_interaction(self, action_type: str, delay: float, 
                       metadata: Dict = None) -> None:
        """
        Registra interacción para análisis longitudinal
        
        Propósito: Trazabilidad ética en investigación UX
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'delay': delay,
            'metadata': metadata or {},
            'research_context': self.research_context
        }
        
        self.interaction_log.append(log_entry)
    
    def export_data(self, format_type: str = "csv") -> str:
        """
        Exporta datos para análisis estadístico en investigación UX
        
        Args:
            format_type: 'csv' o 'json'
            
        Returns:
            Ruta del archivo exportado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format_type == "csv":
            filename = f"interaction_data_{timestamp}.csv"
            
            # Preparar datos para CSV
            csv_data = []
            for entry in self.interaction_log:
                csv_data.append({
                    'timestamp': entry['timestamp'],
                    'action_type': entry['action_type'],
                    'delay': entry['delay'],
                    'research_context': entry['research_context'],
                    'metadata': json.dumps(entry['metadata'])
                })
            
            df = pd.DataFrame(csv_data)
            df.to_csv(filename, index=False)
            
        elif format_type == "json":
            filename = f"interaction_data_{timestamp}.json"
            
            export_data = {
                'research_context': self.research_context,
                'export_timestamp': datetime.now().isoformat(),
                'data': self.interaction_log
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2)
        
        return filename

# Ejemplo de uso para investigación UX
if __name__ == "__main__":
    # Inicializar modelo para investigación
    model = InteractionPatternModel("Estudio_Accesibilidad_2024")
    
    # Texto de ejemplo para análisis
    sample_text = "Usuario completando formulario de registro en aplicación web"
    
    print("=== SIMULACIÓN DE PATRONES DE INTERACCIÓN HUMANA ===")
    print("Propósito: Investigación en UX y accesibilidad digital\n")
    
    # Simular diferentes perfiles de usuario
    for profile_name in model.user_profiles.keys():
        print(f"\n--- Perfil: {profile_name.replace('_', ' ').title()} ---")
        
        # Ejecutar simulación
        session_data = model.simulate_session(profile_name, sample_text)
        
        # Mostrar análisis cognitivo
        cognitive_analysis = session_data['cognitive_analysis']
        print(f"Tiempo promedio de respuesta: {cognitive_analysis['avg_response_time']:.2f}s")
        print(f"Distribución carga cognitiva: {cognitive_analysis['cognitive_load_distribution']}")
        print(f"Tasa de errores: {cognitive_analysis['error_rate']:.2%}")
        
        # Métricas de accesibilidad
        accessibility = session_data['accessibility_metrics']
        print(f"Acciones con alta carga cognitiva: {accessibility['high_cognitive_load_percentage']:.1f}%")
        
        if accessibility['recommended_interface_adaptations']:
            print("Recomendaciones de adaptación:")
            for recommendation in accessibility['recommended_interface_adaptations']:
                print(f"  • {recommendation}")
    
    print("\n=== NOTAS ÉTICAS ===")
    print("• Datos sintéticos generados para investigación UX")
    print("• Propósito: Mejorar accesibilidad y diseño adaptativo")
    print("• No replicar comportamiento real sin consentimiento")
    print("• Uso exclusivo para optimización de experiencia de usuario")