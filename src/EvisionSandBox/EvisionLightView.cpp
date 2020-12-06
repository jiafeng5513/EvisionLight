#include "EvisionLightView.h"

EvisionLightView::EvisionLightView()
{
}

EvisionLightView::~EvisionLightView()
{
}
/// <summary>
/// 
/// </summary>
/// <returns></returns>
EvisionLightView* EvisionLightView::EvisionLightViewFactory()
{
	if (m_pInstance == NULL)
		m_pInstance = new EvisionLightView();
	return m_pInstance;
}
/// <summary>
/// 显示所有被启动的窗口
/// </summary>
void EvisionLightView::show_windows()
{
    ShowAppMainMenuBar();
	if (this->show_demo_window)
	{
		DemoWindow();
	}
	if (this->show_Setting_window)
	{
		SettingWindow();
	}
}
/// <summary>
/// 获取窗口背景颜色
/// </summary>
/// <returns></returns>
ImVec4 EvisionLightView::getWindowColor()
{
    return clear_color;
}
/// <summary>
/// 开启Demo窗口
/// </summary>
void EvisionLightView::DrawDemoWindow()
{
	this->show_demo_window = true;
}
/// <summary>
/// 隐藏Demo窗口
/// </summary>
void EvisionLightView::HideDemoWindow()
{
	this->show_demo_window = false;
}
/// <summary>
/// 开启Setting窗口
/// </summary>
void EvisionLightView::DrawSettingWindow()
{
	this->show_Setting_window = true;
}
/// <summary>
/// 隐藏Setting窗口
/// </summary>
void EvisionLightView::HideSettingWindow()
{
	this->show_Setting_window = false;
}
/// <summary>
/// 定义Demo窗口
/// </summary>
void EvisionLightView::DemoWindow()
{
	ImGui::ShowDemoWindow(&show_demo_window);
}
/// <summary>
/// 定义设置窗口
/// </summary>
void EvisionLightView::SettingWindow()
{
    static float f = 0.0f;
    static int counter = 0;

    ImGui::Begin("Window Status",&show_Setting_window);         // Create a window called "Hello, world!" and append into it.
    ImGui::Text(u8"Backend : GLFW+OpenGL2");
    ImGui::ColorEdit3(u8"窗口颜色编辑", (float*)&clear_color); // Edit 3 floats representing a color
    //ImGui::SameLine();
    ImGui::Text(u8"帧率 %.3f ms/frame (%.1f FPS)", 1000.0f / ImGui::GetIO().Framerate, ImGui::GetIO().Framerate);
    ImGui::End();
}
/// <summary>
/// 定义菜单栏
/// </summary>
void EvisionLightView::ShowAppMainMenuBar()
{
    if (ImGui::BeginMainMenuBar())
    {
        if (ImGui::BeginMenu(u8"工具")) {
            if (ImGui::MenuItem(u8"双目相机")) {}
            if (ImGui::MenuItem(u8"单目相机")) {}
            if (ImGui::MenuItem(u8"Matlab参数传递")) {}
            ImGui::Separator();
            if (ImGui::MenuItem(u8"点云查看器")) {}
            if (ImGui::MenuItem(u8"视差转点云")) {}
            ImGui::Separator();
            if (ImGui::MenuItem(u8"*RealSense")) {}
            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu(u8"单目相机")) {
            if (ImGui::MenuItem(u8"单目标定")) {}
            if (ImGui::MenuItem(u8"几何体追踪", "CTRL+Z")) {}
            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu(u8"双目相机")) {
            if (ImGui::MenuItem(u8"双目标定")) {}
            if (ImGui::MenuItem(u8"矫正")) {}
            if (ImGui::MenuItem(u8"视差")) {}
            if (ImGui::MenuItem(u8"视觉测量")) {}
            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu(u8"Ai")) {
            if (ImGui::MenuItem(u8"目标检测")) {}
            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu(u8"帮助")) {
            if (ImGui::MenuItem(u8"帮助信息", "CTRL+Z")) {}
            if (ImGui::MenuItem(u8"About Evision")) {}
            if (ImGui::MenuItem(u8"Log View")) {}
            ImGui::EndMenu();
        }
        if (ImGui::BeginMenu(u8"窗口")) {
            if (ImGui::MenuItem(u8"Demo")) {
                this->DrawDemoWindow();
            }
            if (ImGui::MenuItem(u8"设置")) {
                this->DrawSettingWindow();
            }
            ImGui::EndMenu();
        }

        if (ImGui::BeginMenu("Edit"))
        {
            if (ImGui::MenuItem("Undo", "CTRL+Z")) {}
            if (ImGui::MenuItem("Redo", "CTRL+Y", false, false)) {}  // Disabled item
            ImGui::Separator();
            if (ImGui::MenuItem("Cut", "CTRL+X")) {}
            if (ImGui::MenuItem("Copy", "CTRL+C")) {}
            if (ImGui::MenuItem("Paste", "CTRL+V")) {}
            ImGui::EndMenu();
        }
        ImGui::EndMainMenuBar();
    }
}