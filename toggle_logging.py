#!/usr/bin/env python3
"""
Script para habilitar/deshabilitar el logging de acciones
"""

import sys
import os

def toggle_logging(enable=None):
    """Habilita o deshabilita el logging de acciones"""
    
    if enable is None:
        current = os.environ.get('ENABLE_ACTION_LOGGING', 'false').lower() == 'true'
        print(f"🔧 Estado actual del logging: {'ENABLED' if current else 'DISABLED'}")
        
        choice = input("¿Habilitar logging? (y/n): ").lower().strip()
        enable = choice in ['y', 'yes', 's', 'si', '1']
    
    status = 'true' if enable else 'false'
    
    print(f"\n🔄 {'Habilitando' if enable else 'Deshabilitando'} logging de acciones...")
    
    # Crear archivo de configuración
    env_content = f"""# Configuración de logging de acciones
export ENABLE_ACTION_LOGGING={status}
export LOGGING_DEBUG=false

# Para aplicar:
# source logging_config.sh
# python3 dashboard.py
"""
    
    with open('logging_config.sh', 'w') as f:
        f.write(env_content)
    
    print(f"✅ Configuración guardada en logging_config.sh")
    print(f"🔧 Action Logging: {'ENABLED' if enable else 'DISABLED'}")
    
    print("\n📋 Para aplicar la configuración:")
    print("1. source logging_config.sh")
    print("2. Reinicia el servidor: python3 dashboard.py")
    
    print("\n💡 Comandos rápidos:")
    if enable:
        print("   Deshabilitar: python3 toggle_logging.py off")
    else:
        print("   Habilitar: python3 toggle_logging.py on")
        print("   🚨 NOTA: Solo habilitar cuando el problema esté resuelto")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['on', 'enable', '1', 'true']:
            toggle_logging(True)
        elif arg in ['off', 'disable', '0', 'false']:
            toggle_logging(False)
        else:
            print("❌ Uso: python3 toggle_logging.py [on/off]")
    else:
        toggle_logging()