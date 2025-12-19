#!/usr/bin/env python3
"""
Instagram OSINT API Functions
Funciones para obtener información pública de Instagram
"""

import requests
import json
import sys
from datetime import datetime


def user_info(usrname, verbose=False):
    """
    Obtiene información pública de un usuario de Instagram
    
    Args:
        usrname (str): Nombre de usuario (sin @)
        verbose (bool): Mostrar información detallada de debug
    
    Returns:
        dict: Datos del usuario o None si hay error
    """
    
    # URL de la API pública de Instagram
    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={usrname}"
    
    # Headers para simular un navegador real
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'X-IG-App-ID': '936619743392459',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': f'https://www.instagram.com/{usrname}/',
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.9,es;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    
    try:
        print(f"🔍 Buscando información de: @{usrname}")
        
        if verbose:
            print(f"   URL: {url}")
            print(f"   Headers: {json.dumps(headers, indent=2)}")
        
        # Hacer la solicitud
        resp = requests.get(url, headers=headers, timeout=15)
        
        if verbose:
            print(f"   Status Code: {resp.status_code}")
            print(f"   Content-Type: {resp.headers.get('Content-Type')}")
        
        # Verificar el status code
        if resp.status_code == 404:
            print(f"\n❌ Usuario '@{usrname}' no encontrado")
            print("   Verifica que el nombre de usuario sea correcto")
            return None
            
        elif resp.status_code == 429:
            print(f"\n❌ Límite de solicitudes excedido")
            print("   Instagram ha bloqueado temporalmente las solicitudes")
            print("   Soluciones:")
            print("   • Espera unos minutos e intenta de nuevo")
            print("   • Usa una VPN para cambiar tu IP")
            print("   • Considera usar autenticación con cookies")
            return None
            
        elif resp.status_code != 200:
            print(f"\n❌ Error HTTP {resp.status_code}")
            if verbose:
                print(f"   Respuesta completa:\n{resp.text[:500]}")
            return None
        
        # Verificar que sea JSON
        content_type = resp.headers.get('Content-Type', '')
        if 'application/json' not in content_type:
            print(f"\n❌ La respuesta no es JSON")
            print(f"   Content-Type recibido: {content_type}")
            print(f"   Primeros 300 caracteres de la respuesta:")
            print(f"   {resp.text[:300]}")
            print("\n   Posibles causas:")
            print("   • Instagram detectó el bot y devolvió HTML")
            print("   • El endpoint de la API cambió")
            print("   • Tu IP fue bloqueada")
            return None
        
        # Parsear JSON
        try:
            data = resp.json()
        except json.JSONDecodeError as e:
            print(f"\n❌ Error al parsear JSON: {e}")
            print(f"   Respuesta recibida (primeros 500 chars):")
            print(f"   {resp.text[:500]}")
            return None
        
        # Verificar estructura de datos
        if 'data' not in data or 'user' not in data.get('data', {}):
            print(f"\n❌ Estructura de respuesta inesperada")
            print(f"   Keys recibidas: {list(data.keys())}")
            if verbose:
                print(f"   Datos completos: {json.dumps(data, indent=2)[:1000]}")
            return None
        
        # Extraer información del usuario
        user = data['data']['user']
        
        # Mostrar información formateada
        print("\n" + "=" * 60)
        print("📊 INFORMACIÓN DEL USUARIO")
        print("=" * 60)
        
        print(f"\n👤 Usuario:      @{user.get('username', 'N/A')}")
        print(f"📝 Nombre:       {user.get('full_name', 'N/A')}")
        print(f"🆔 User ID:      {user.get('id', 'N/A')}")
        
        # Estadísticas
        posts = user.get('edge_owner_to_timeline_media', {}).get('count', 0)
        followers = user.get('edge_followed_by', {}).get('count', 0)
        following = user.get('edge_follow', {}).get('count', 0)
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   📸 Posts:        {posts:,}")
        print(f"   👥 Seguidores:   {followers:,}")
        print(f"   ➕ Siguiendo:    {following:,}")
        
        # Calcular engagement rate si tiene seguidores
        if followers > 0:
            engagement = (posts / followers) * 100
            print(f"   📊 Engagement:   {engagement:.2f}%")
        
        # Estado de la cuenta
        print(f"\n🔐 ESTADO:")
        print(f"   {'🔒' if user.get('is_private') else '🔓'} Cuenta:      {'Privada' if user.get('is_private') else 'Pública'}")
        print(f"   {'✅' if user.get('is_verified') else '❌'} Verificada:  {'Sí' if user.get('is_verified') else 'No'}")
        print(f"   {'💼' if user.get('is_business_account') else '👤'} Tipo:        {'Negocio' if user.get('is_business_account') else 'Personal'}")
        
        # Biografía
        bio = user.get('biography', '')
        if bio:
            print(f"\n📄 BIOGRAFÍA:")
            # Dividir bio en líneas si es muy larga
            bio_lines = bio.split('\n')
            for line in bio_lines[:5]:  # Máximo 5 líneas
                print(f"   {line}")
            if len(bio_lines) > 5:
                print(f"   ... (+{len(bio_lines) - 5} líneas más)")
        
        # Link externo
        external_url = user.get('external_url')
        if external_url:
            print(f"\n🔗 LINK EXTERNO:")
            print(f"   {external_url}")
        
        # Categoría de negocio
        category = user.get('category_name')
        if category:
            print(f"\n📂 CATEGORÍA:")
            print(f"   {category}")
        
        # Información adicional si está disponible
        if verbose:
            print(f"\n🔍 INFORMACIÓN ADICIONAL:")
            print(f"   Tiene IGTV:              {user.get('has_channel', False)}")
            print(f"   Clips destacados:        {user.get('highlight_reel_count', 0)}")
            print(f"   Es profesional:          {user.get('is_professional_account', False)}")
            print(f"   Unió recientemente:      {user.get('is_joined_recently', False)}")
        
        print("=" * 60)
        
        return user
        
    except requests.exceptions.Timeout:
        print(f"\n❌ Timeout: Instagram no respondió a tiempo")
        print("   Intenta de nuevo en unos segundos")
        return None
        
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Error de conexión")
        print("   Verifica tu conexión a internet")
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Error en la solicitud: {e}")
        return None
        
    except Exception as e:
        print(f"\n❌ Error inesperado: {type(e).__name__}: {e}")
        if verbose:
            import traceback
            traceback.print_exc()
        return None


def post_info(user_data=None, verbose=False):
    """
    Obtiene información de los posts de un usuario
    
    Args:
        user_data (dict): Datos del usuario obtenidos de user_info()
        verbose (bool): Mostrar información detallada
    """
    
    if user_data is None:
        print("\n⚠️ No hay datos de usuario disponibles")
        return
    
    username = user_data.get('username', 'unknown')
    
    print(f"\n📸 INFORMACIÓN DE POSTS DE @{username}")
    print("-" * 60)
    
    # Verificar si la cuenta es privada
    if user_data.get('is_private'):
        print("🔒 La cuenta es privada")
        print("   No se puede acceder a los posts sin autenticación")
        return
    
    # Obtener posts desde edge_owner_to_timeline_media
    timeline = user_data.get('edge_owner_to_timeline_media', {})
    posts = timeline.get('edges', [])
    
    if not posts:
        print("📭 El usuario no tiene posts públicos")
        return
    
    print(f"Total de posts encontrados: {len(posts)}")
    print()
    
    # Mostrar información de cada post
    for i, post_edge in enumerate(posts[:12], 1):  # Mostrar máximo 12 posts
        post = post_edge.get('node', {})
        
        print(f"Post #{i}:")
        print(f"  🆔 ID:           {post.get('id', 'N/A')}")
        print(f"  📅 Fecha:        {datetime.fromtimestamp(post.get('taken_at_timestamp', 0)).strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"  ❤️  Likes:        {post.get('edge_liked_by', {}).get('count', 0):,}")
        print(f"  💬 Comentarios:  {post.get('edge_media_to_comment', {}).get('count', 0):,}")
        
        # Tipo de post
        if post.get('is_video'):
            print(f"  🎥 Tipo:         Video")
            print(f"  ⏱️  Duración:     {post.get('video_duration', 0):.1f}s")
            print(f"  👁️  Vistas:       {post.get('video_view_count', 0):,}")
        else:
            print(f"  🖼️  Tipo:         Imagen")
        
        # Caption (primeras líneas)
        caption_edges = post.get('edge_media_to_caption', {}).get('edges', [])
        if caption_edges:
            caption = caption_edges[0].get('node', {}).get('text', '')
            if caption:
                caption_preview = caption[:100].replace('\n', ' ')
                print(f"  📝 Caption:      {caption_preview}{'...' if len(caption) > 100 else ''}")
        
        # URL del post
        shortcode = post.get('shortcode')
        if shortcode:
            print(f"  🔗 URL:          https://www.instagram.com/p/{shortcode}/")
        
        print()
    
    # Estadísticas generales
    if len(posts) > 0:
        total_likes = sum(p.get('node', {}).get('edge_liked_by', {}).get('count', 0) for p in posts)
        total_comments = sum(p.get('node', {}).get('edge_media_to_comment', {}).get('count', 0) for p in posts)
        avg_likes = total_likes / len(posts)
        avg_comments = total_comments / len(posts)
        
        print("-" * 60)
        print("📊 ESTADÍSTICAS DE POSTS:")
        print(f"   Promedio de likes:       {avg_likes:,.0f}")
        print(f"   Promedio de comentarios: {avg_comments:,.0f}")
        print(f"   Total de interacciones:  {total_likes + total_comments:,}")
        print("-" * 60)


# Función auxiliar para formato de números grandes
def format_number(num):
    """Formatea números grandes (ejemplo: 1500000 -> 1.5M)"""
    if num >= 1_000_000:
        return f"{num/1_000_000:.1f}M"
    elif num >= 1_000:
        return f"{num/1_000:.1f}K"
    else:
        return str(num)