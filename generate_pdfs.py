import asyncio
from playwright.async_api import async_playwright
import os

async def generar_cvs():
    # Asegurarnos de que el directorio data exista
    os.makedirs("data", exist_ok=True)

    # Configuración de los CVs a generar
    curriculums = [
        {
            "nombre": "CV Principal",
            "url": "https://savingl.cl/cv-guillermoleon",
            "output": "data/cv_pdf/cv-principal-es.pdf"
        },
    ]
    
    async with async_playwright() as p:
        # Lanzamos el navegador en modo 'oculto' (headless)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        for cv in curriculums:
            print(f"[INFO] Cargando '{cv['nombre']}' desde {cv['url']}...")
            try:
                # Vamos a la página y esperamos hasta que la red esté inactiva
                await page.goto(cv["url"], wait_until="networkidle")
                
                # Esperamos a que el div interactivo y el contenido de markdown estén visibles
                # (Esto asegura que tu JS ya terminó de hacer el fetch e inyectó el HTML renderizado)
                await page.wait_for_selector("#cv-content", state="visible", timeout=10000)
                
                # Extra de 1 segundo para estabilizar estilos y fuentes del navegador
                await page.wait_for_timeout(1000) 
                
                # Generamos el PDF usando @media print activado por defecto
                await page.pdf(
                    path=cv["output"],
                    format="A4",
                    print_background=True # Indispensable para que apliquen detalles gráficos y CSS correctamente
                )
                print(f"[EXITO] PDF guardado en: {cv['output']}\n")
                
            except Exception as e:
                print(f"[ERROR] Ocurrió un error al procesar {cv['nombre']}:\n{e}\n")
                
        await browser.close()
        print("[FIN] Proceso finalizado.")

if __name__ == "__main__":
    asyncio.run(generar_cvs())
