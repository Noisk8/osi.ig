#!/usr/bin/env python3
"""
Instagram OSINT Tool - Main Script
Herramienta para obtener información pública de usuarios de Instagram
"""

import os
import sys
import argparse

# Añadir directorio de librerías al path
sys.path.append(os.path.join(os.getcwd(), ".lib"))

try:
    from api import user_info, post_info
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("Asegúrate de que el archivo .lib/api.py existe")
    sys.exit(1)


def main():
    """Función principal del programa"""
    
    # Configurar argumentos de línea de comandos
    ap = argparse.ArgumentParser(
        description="Instagram OSINT Tool - Obtiene información pública de usuarios",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python main.py -u instagram
  python main.py -u nasa -p
  python main.py --user cristiano --post
        """
    )
    
    ap.add_argument(
        "-u", "--user", 
        required=True, 
        help="Nombre de usuario (sin @) de la cuenta a escanear"
    )
    
    ap.add_argument(
        "-p", "--post", 
        action="store_true", 
        help="Mostrar información de posts del usuario"
    )
    
    ap.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Modo verbose (más detalles)"
    )
    
    # Parsear argumentos
    args = ap.parse_args()
    
    # Limpiar pantalla
    os.system("clear" if os.name != "nt" else "cls")
    
    # Banner
    print("=" * 60)
    print(" 🔍 INSTAGRAM OSINT TOOL")
    print("=" * 60)
    print()
    
    # Obtener información del usuario
    if args.user:
        try:
            user_data = user_info(usrname=args.user, verbose=args.verbose)
            
            if user_data is None:
                print("\n⚠️ No se pudo obtener información del usuario")
                print("Posibles causas:")
                print("  • El usuario no existe")
                print("  • Instagram bloqueó la solicitud")
                print("  • Problemas de conexión")
                sys.exit(1)
            
            # Obtener información de posts si se solicita
            if args.post:
                print("\n" + "-" * 60)
                post_info(user_data=user_data, verbose=args.verbose)
                
        except KeyboardInterrupt:
            print("\n\n⚠️ Operación cancelada por el usuario")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error inesperado: {type(e).__name__}: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ Escaneo completado")
    print("=" * 60)


if __name__ == "__main__":
    main()