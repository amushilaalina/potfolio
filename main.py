import os
import json
import time
# pyrefly: ignore [missing-import]
import flet as ft

# Helper to format display names from filenames
def display_name_from_filename(filename):
    basename = os.path.basename(filename)
    name_without_ext, _ = os.path.splitext(basename)
    # Clean up (1) or (2) if present
    name_clean = name_without_ext.replace("(1)", "").replace("(2)", "")
    name_clean = name_clean.replace("_", " ").replace("-", " ")
    name_clean = " ".join(name_clean.split())
    return name_clean.title()

# Helper to scan assets with fallbacks
def get_asset_files(folder, extensions):
    # 1. Try local filesystem
    local_path = os.path.join("assets", folder)
    if os.path.exists(local_path) and os.path.isdir(local_path):
        files = []
        for root, _, filenames in os.walk(local_path):
            for f in filenames:
                if any(f.lower().endswith(ext) for ext in extensions):
                    rel = os.path.relpath(os.path.join(root, f), "assets").replace("\\", "/")
                    files.append(rel)
        if files:
            return sorted(files)
            
    # 2. Try reading manifest.json
    manifest_paths = ["assets/manifest.json", "manifest.json"]
    for manifest_path in manifest_paths:
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r") as f:
                    manifest = json.load(f)
                    if folder in manifest:
                        files = [f for f in manifest[folder] if any(f.lower().endswith(ext) for ext in extensions)]
                        if files:
                            return sorted(files)
            except Exception:
                pass
                
    # 3. Fallback to audited list
    if folder == "certificates":
        return sorted([
            "certificates/matlab/Exprolereport.pdf",
            "certificates/matlab/Matricesreport (1).pdf",
            "certificates/matlab/Matricesreport.pdf",
            "certificates/matlab/MOcertificate (1).pdf",
            "certificates/matlab/MOreport.pdf",
            "certificates/matlab/SF.pdf",
            "certificates/matlab/SFreport.pdf",
            "certificates/matlab/SOcertificate.pdf",
            "certificates/matlab/SOreport.pdf"
        ])
    elif folder == "videos":
        return ["videos/contribution-video.mp4"]
    elif folder == "pictures":
        return ["pictures/profile.jpeg"]
    return []

# Autogenerate manifest file when running locally
def generate_manifest():
    if os.path.exists("assets"):
        manifest = {}
        for folder in ["certificates", "pictures", "videos"]:
            folder_path = os.path.join("assets", folder)
            manifest[folder] = []
            if os.path.exists(folder_path):
                for root, _, filenames in os.walk(folder_path):
                    for f in filenames:
                        rel = os.path.relpath(os.path.join(root, f), "assets").replace("\\", "/")
                        manifest[folder].append(rel)
        try:
            with open("assets/manifest.json", "w") as f:
                json.dump(manifest, f, indent=2)
        except Exception as e:
            print(f"Error generating manifest: {e}")

def main(page: ft.Page):
    # Setup manifest file locally
    generate_manifest()

    # Page settings
    page.title = "Alina Amushila | Portfolio"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "#0B0F19"  # Rich dark charcoal/navy
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.padding = 0
    page.spacing = 0

    # Custom font from Google Fonts
    page.fonts = {
        "Outfit": "https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap"
    }
    page.theme = ft.Theme(font_family="Outfit")

    # Colors
    accent_color = "#F59E0B"  # Warm amber/gold
    card_bg = "#111827"       # Dark grey card
    bg_nav = "#0F172A"        # Slate navy
    text_primary = "#F8FAFC"  # Slate white
    text_secondary = "#94A3B8"# Slate gray

    # Splash Screen
    splash = ft.Container(
        content=ft.Column(
            [
                ft.ProgressRing(width=55, height=55, stroke_width=4, color=accent_color),
                ft.Text("Loading portfolio evidence...", size=16, color=text_primary, weight=ft.FontWeight.W_500),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=20
        ),
        alignment=ft.Alignment(0, 0),
        bgcolor="#0B0F19",
        expand=True,
        height=600  # Give a height for initial load
    )
    
    page.add(splash)
    page.update()
    
    # Simulate scanning and setup
    time.sleep(1.2)
    
    # Clear splash
    page.controls.clear()

    # Helper for navigation scrolling
    def scroll_to_section(e):
        key = e.control.data
        page.scroll_to(key=key, duration=600)

    # 1. Navigation Header
    nav_links = [
        ft.TextButton("About", data="about", on_click=scroll_to_section, style=ft.ButtonStyle(color=text_primary)),
        ft.TextButton("Skills", data="skills", on_click=scroll_to_section, style=ft.ButtonStyle(color=text_primary)),
        ft.TextButton("Projects", data="projects", on_click=scroll_to_section, style=ft.ButtonStyle(color=text_primary)),
        ft.TextButton("Certificates", data="certificates", on_click=scroll_to_section, style=ft.ButtonStyle(color=text_primary)),
        ft.TextButton("Reflection Video", data="video", on_click=scroll_to_section, style=ft.ButtonStyle(color=text_primary)),
    ]

    navbar = ft.Container(
        content=ft.ResponsiveRow(
            [
                ft.Column(
                    [
                        ft.Text("Alina Amushila", size=22, weight=ft.FontWeight.BOLD, color=accent_color),
                    ],
                    col={"xs": 12, "md": 4},
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.START
                ),
                ft.Column(
                    [
                        ft.Row(
                            nav_links,
                            alignment=ft.MainAxisAlignment.END,
                            wrap=True
                        )
                    ],
                    col={"xs": 12, "md": 8},
                    alignment=ft.MainAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor=bg_nav,
        padding=ft.Padding(30, 15, 30, 15),
        shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.3)", offset=ft.Offset(0, 4))
    )

    # 2. Hero Section
    # Find profile picture
    pic_files = get_asset_files("pictures", [".jpg", ".jpeg", ".png", ".webp"])
    profile_pic = pic_files[0] if pic_files else "pictures/profile.jpeg"

    hero_text = ft.Column(
        [
            ft.Container(
                content=ft.Text("STUDENT PORTFOLIO", size=12, color=accent_color, weight=ft.FontWeight.BOLD),
                bgcolor="rgba(245, 158, 11, 0.1)",
                padding=ft.Padding(12, 6, 12, 6),
                border_radius=20,
                border=ft.Border(ft.BorderSide(1, "rgba(245, 158, 11, 0.3)"), ft.BorderSide(1, "rgba(245, 158, 11, 0.3)"), ft.BorderSide(1, "rgba(245, 158, 11, 0.3)"), ft.BorderSide(1, "rgba(245, 158, 11, 0.3)"))
            ),
            ft.Text("Alina Amushila", size=48, weight=ft.FontWeight.BOLD, color=text_primary, height=55),
            ft.Text(
                "Engineering Student | Programmer | Technology Enthusiast",
                size=18,
                color=text_secondary,
                weight=ft.FontWeight.W_400
            ),
            ft.Divider(color="rgba(255,255,255,0.1)", height=20),
            ft.Row(
                [
                    ft.Icon(ft.icons.Icons.EMAIL, color=accent_color, size=18),
                    ft.Text("alinapraiseamushila@gmail.com", color=text_primary, size=15),
                ],
                spacing=10
            ),
            ft.Row(
                [
                    ft.Icon(ft.icons.Icons.CODE, color=accent_color, size=18),
                    ft.Text("GitHub: amushilaalina", color=text_primary, size=15),
                ],
                spacing=10
            ),
            ft.Row(
                [
                    ft.ElevatedButton(
                        "View Certificates",
                        icon=ft.icons.Icons.CARD_MEMBERSHIP,
                        color="#0B0F19",
                        bgcolor=accent_color,
                        data="certificates",
                        on_click=scroll_to_section,
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=8),
                            padding=ft.Padding(20, 16, 20, 16)
                        )
                    ),
                    ft.OutlinedButton(
                        "Watch Reflection Video",
                        icon=ft.icons.Icons.PLAY_ARROW,
                        data="video",
                        on_click=scroll_to_section,
                        style=ft.ButtonStyle(
                            color=accent_color,
                            shape=ft.RoundedRectangleBorder(radius=8),
                            side={"": ft.BorderSide(2, accent_color)},
                            padding=ft.Padding(20, 16, 20, 16)
                        )
                    )
                ],
                spacing=15,
                wrap=True
            )
        ],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER
    )

    hero_image = ft.Container(
        content=ft.Image(
            src=profile_pic,
            fit='cover',
            border_radius=20,
        ),
        width=300,
        height=320,
        border_radius=20,
        border=ft.Border(ft.BorderSide(3, accent_color), ft.BorderSide(3, accent_color), ft.BorderSide(3, accent_color), ft.BorderSide(3, accent_color)),
        shadow=ft.BoxShadow(blur_radius=25, color="rgba(245, 158, 11, 0.25)"),
        alignment=ft.Alignment(0, 0)
    )

    hero_section = ft.Container(
        content=ft.ResponsiveRow(
            [
                ft.Column([hero_text], col={"xs": 12, "md": 7}, alignment=ft.MainAxisAlignment.CENTER),
                ft.Column([hero_image], col={"xs": 12, "md": 5}, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.CENTER)
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=30
        ),
        padding=ft.Padding(20, 40, 20, 40),
    )

    # 3. About Section
    about_section = ft.Container(
        key="about",
        content=ft.Column(
            [
                ft.Text("About Me", size=28, weight=ft.FontWeight.BOLD, color=accent_color),
                ft.Text(
                    "Hello, my name is Alina Amushila. I am a student at the University of Namibia (UNAM) with a strong interest in programming, engineering, and technology. I enjoy solving real-world problems through software development and continuously improving my technical skills.",
                    size=16,
                    color=text_primary
                ),
                ft.Text(
                    "This portfolio showcases my academic progress, MATLAB certificates, contribution video, and project evidence gathered throughout my studies, specifically for the Computer Programming I course.",
                    size=16,
                    color=text_secondary
                )
            ],
            spacing=15
        ),
        bgcolor=card_bg,
        padding=30,
        border_radius=12,
        border=ft.Border(left=ft.BorderSide(4, accent_color)),
        shadow=ft.BoxShadow(blur_radius=15, color="rgba(0,0,0,0.2)")
    )

    # 4. Technical Skills Section
    skills_list = [
        "HTML & CSS", "JavaScript", "Python Programming", "C Programming",
        "Problem Solving", "Software Development", "Git & GitHub", "Database Fundamentals"
    ]
    
    skills_chips = []
    for skill in skills_list:
        skills_chips.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Container(width=8, height=8, bgcolor=accent_color, shape=ft.BoxShape.CIRCLE),
                        ft.Text(skill, size=14, color=text_primary, weight=ft.FontWeight.W_500)
                    ],
                    spacing=8,
                    tight=True
                ),
                bgcolor=card_bg,
                padding=ft.Padding(15, 8, 15, 8),
                border_radius=8,
                border=ft.Border(ft.BorderSide(1, "rgba(255,255,255,0.1)"), ft.BorderSide(1, "rgba(255,255,255,0.1)"), ft.BorderSide(1, "rgba(255,255,255,0.1)"), ft.BorderSide(1, "rgba(255,255,255,0.1)"))
            )
        )

    skills_section = ft.Container(
        key="skills",
        content=ft.Column(
            [
                ft.Text("Technical Skills", size=28, weight=ft.FontWeight.BOLD, color=accent_color),
                ft.Text("A compilation of tools, frameworks, and engineering competencies I have practiced.", size=16, color=text_secondary),
                ft.Divider(color="rgba(255,255,255,0.1)", height=15),
                ft.Row(
                    skills_chips,
                    wrap=True,
                    spacing=12,
                    run_spacing=12
                )
            ],
            spacing=15
        ),
        padding=20
    )

    # 5. Projects Section
    projects = [
        {
            "title": "Semester Programming Project",
            "desc": "Developed a software solution as part of the Computer Programming I semester project. The project focused on applying programming concepts to solve real-world engineering challenges.",
            "icon": ft.icons.Icons.ASSIGNMENT
        },
        {
            "title": "Programming Assignments",
            "desc": "Completed multiple programming assignments involving algorithms, data processing, user interfaces, and software design principles.",
            "icon": ft.icons.Icons.CODE_OFF
        }
    ]

    project_cards = []
    for p in projects:
        project_cards.append(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(p["icon"], color=accent_color, size=28),
                                        ft.Text(p["title"], size=20, weight=ft.FontWeight.BOLD, color=text_primary),
                                    ],
                                    spacing=10
                                ),
                                ft.Text(p["desc"], size=15, color=text_secondary),
                                ft.Container(
                                    content=ft.Text("Portfolio Evidence", size=12, color=accent_color, weight=ft.FontWeight.W_600),
                                    bgcolor="rgba(245, 158, 11, 0.1)",
                                    padding=ft.Padding(10, 4, 10, 4),
                                    border_radius=5
                                )
                            ],
                            spacing=15,
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        ),
                        bgcolor=card_bg,
                        padding=25,
                        border_radius=12,
                        border=ft.Border(ft.BorderSide(1, "rgba(255,255,255,0.05)"), ft.BorderSide(1, "rgba(255,255,255,0.05)"), ft.BorderSide(1, "rgba(255,255,255,0.05)"), ft.BorderSide(1, "rgba(255,255,255,0.05)")),
                        expand=True,
                        shadow=ft.BoxShadow(blur_radius=10, color="rgba(0,0,0,0.15)")
                    )
                ],
                col={"xs": 12, "md": 6}
            )
        )

    projects_section = ft.Container(
        key="projects",
        content=ft.Column(
            [
                ft.Text("Projects & Coursework", size=28, weight=ft.FontWeight.BOLD, color=accent_color),
                ft.Text("Key software projects and academic assignments demonstrating practical coding skill.", size=16, color=text_secondary),
                ft.Divider(color="rgba(255,255,255,0.1)", height=15),
                ft.ResponsiveRow(
                    project_cards,
                    spacing=20,
                    run_spacing=20
                )
            ],
            spacing=15
        ),
        padding=20
    )

    # 6. Certificates Section
    cert_files = get_asset_files("certificates", [".pdf", ".png", ".jpg", ".jpeg", ".webp"])
    cert_cards = []
    
    for cert in cert_files:
        display_name = display_name_from_filename(cert)
        is_pdf = cert.lower().endswith(".pdf")
        
        # Build URL for launching
        # Use relative asset path
        cert_url = cert

        card_content = ft.Column(
            [
                ft.Container(
                    content=ft.Icon(
                        ft.icons.Icons.PICTURE_AS_PDF if is_pdf else ft.icons.Icons.IMAGE,
                        color=accent_color if is_pdf else ft.Colors.GREEN_ACCENT,
                        size=40
                    ),
                    alignment=ft.Alignment(0, 0),
                    height=100,
                    bgcolor="rgba(255,255,255,0.03)",
                    border_radius=8
                ),
                ft.Column(
                    [
                        ft.Text(display_name, size=15, weight=ft.FontWeight.BOLD, color=text_primary, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                        ft.Text("MATLAB Training" if "matlab" in cert.lower() else "Certificate", size=13, color=text_secondary),
                    ],
                    spacing=5,
                    height=50
                ),
                ft.TextButton(
                    "View Certificate",
                    icon=ft.icons.Icons.OPEN_IN_NEW,
                    icon_color=accent_color,
                    style=ft.ButtonStyle(color=accent_color),
                    url=cert_url
                )
            ],
            spacing=12,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )

        cert_cards.append(
            ft.Container(
                content=card_content,
                bgcolor=card_bg,
                padding=15,
                border_radius=10,
                border=ft.Border(ft.BorderSide(1, "rgba(255,255,255,0.05)"), ft.BorderSide(1, "rgba(255,255,255,0.05)"), ft.BorderSide(1, "rgba(255,255,255,0.05)"), ft.BorderSide(1, "rgba(255,255,255,0.05)")),
                col={"xs": 12, "sm": 6, "md": 4},
                shadow=ft.BoxShadow(blur_radius=8, color="rgba(0,0,0,0.1)")
            )
        )

    # Fallback if no certificates found
    if not cert_cards:
        cert_cards.append(
            ft.Container(
                content=ft.Text("No certificates found in assets/certificates.", color=text_secondary, size=16),
                padding=20,
                col={"xs": 12}
            )
        )

    certificates_section = ft.Container(
        key="certificates",
        content=ft.Column(
            [
                ft.Text("Certificates & Achievements", size=28, weight=ft.FontWeight.BOLD, color=accent_color),
                ft.Text("Verified professional qualifications and training program completions.", size=16, color=text_secondary),
                ft.Divider(color="rgba(255,255,255,0.1)", height=15),
                ft.ResponsiveRow(
                    cert_cards,
                    spacing=20,
                    run_spacing=20
                )
            ],
            spacing=15
        ),
        padding=20
    )

    # 7. Reflection Video Section
    video_files = get_asset_files("videos", [".mp4", ".mov", ".webm"])
    video_content = None

    if video_files:
        video_url = video_files[0]
        # Embedded Flet Video Player if supported
        has_video_control = hasattr(ft, "Video")
        if has_video_control:
            try:
                video_content = ft.Container(
                    content=ft.Video(
                        expand=True,
                        playlist=[ft.VideoMedia(video_url)],
                        playlist_mode=ft.PlaylistMode.LOOP,
                        aspect_ratio=16/9,
                        volume=100,
                        autoplay=False,
                        show_controls=True,
                    ),
                    border_radius=12,
                    border=ft.Border(ft.BorderSide(1, "rgba(255,255,255,0.1)"), ft.BorderSide(1, "rgba(255,255,255,0.1)"), ft.BorderSide(1, "rgba(255,255,255,0.1)"), ft.BorderSide(1, "rgba(255,255,255,0.1)")),
                    shadow=ft.BoxShadow(blur_radius=15, color="rgba(0,0,0,0.3)"),
                    alignment=ft.Alignment(0, 0)
                )
            except Exception as e:
                has_video_control = False
                
        if not has_video_control:
            # Fallback if Video control throws an error or is not supported
            video_content = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.Icons.VIDEO_LIBRARY, size=50, color=accent_color),
                        ft.Text("Reflection Video File", size=18, weight=ft.FontWeight.BOLD, color=text_primary),
                        ft.Text(f"File: {video_url}", size=14, color=text_secondary),
                        ft.ElevatedButton(
                            "Open Reflection Video",
                            icon=ft.icons.Icons.PLAY_CIRCLE,
                            color="#0B0F19",
                            bgcolor=accent_color,
                            url=video_url,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=10
                ),
                padding=30,
                bgcolor=card_bg,
                border_radius=12,
                alignment=ft.Alignment(0, 0)
            )
    else:
        video_content = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.icons.Icons.PLAY_DISABLED, size=40, color=text_secondary),
                    ft.Text("No contribution video found in assets/videos.", color=text_secondary, size=15),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER
            ),
            bgcolor=card_bg,
            padding=40,
            border_radius=12,
            alignment=ft.Alignment(0, 0)
        )

    video_section = ft.Container(
        key="video",
        content=ft.Column(
            [
                ft.Text("Technical Blog & Reflection Video", size=28, weight=ft.FontWeight.BOLD, color=accent_color),
                ft.Text(
                    "My semester project reflection video, sharing project contributions, engineering learnings, and technical development insights.",
                    size=16,
                    color=text_secondary
                ),
                ft.Divider(color="rgba(255,255,255,0.1)", height=15),
                ft.Container(
                    content=video_content,
                    alignment=ft.Alignment(0, 0),
                    padding=ft.Padding(0, 10, 0, 0)
                )
            ],
            spacing=15
        ),
        padding=20
    )

    # 8. Footer
    footer = ft.Container(
        content=ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Alina Amushila", size=16, weight=ft.FontWeight.BOLD, color=text_primary),
                        ft.Text("|", size=16, color="rgba(255,255,255,0.2)"),
                        ft.Text("2026 Student Portfolio", size=14, color=text_secondary),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10
                ),
                ft.Row(
                    [
                        ft.TextButton("GitHub: amushilaalina", url="https://github.com/amushilaalina", style=ft.ButtonStyle(color=text_secondary)),
                        ft.TextButton("Email", url="mailto:alinapraiseamushila@gmail.com", style=ft.ButtonStyle(color=text_secondary))
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=15
                )
            ],
            spacing=10,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        bgcolor="#070A10",
        padding=ft.Padding(25, 25, 25, 25),
        border=ft.Border(top=ft.BorderSide(1, "rgba(255,255,255,0.05)"))
    )

    # Main wrapper container to limit maximum width on wide displays
    content_wrapper = ft.Container(
        content=ft.Column(
            [
                hero_section,
                ft.Container(height=10),
                about_section,
                ft.Container(height=10),
                skills_section,
                ft.Container(height=10),
                projects_section,
                ft.Container(height=10),
                certificates_section,
                ft.Container(height=10),
                video_section,
                ft.Container(height=20),
            ],
            spacing=30,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.Alignment(0, 0),
        padding=ft.Padding(15, 0, 15, 0)
    )

    # Scroll top FAB
    def go_top(e):
        page.scroll_to(delta=0, duration=600)

    fab = ft.FloatingActionButton(
        icon=ft.icons.Icons.ARROW_UPWARD,
        bgcolor=accent_color,
        foreground_color="#0B0F19",
        mini=True,
        on_click=go_top,
        tooltip="Back to Top"
    )

    # Add components to page
    page.add(
        navbar,
        ft.Row([content_wrapper], alignment=ft.MainAxisAlignment.CENTER),
        footer
    )
    page.floating_action_button = fab
    page.update()

# Run application
if __name__ == "__main__":
    ft.app(target=main, assets_dir="assets")
