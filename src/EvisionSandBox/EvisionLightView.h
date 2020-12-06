#include "imgui.h"

/// <summary>
/// 主界面管理器,做单例工厂
/// </summary>
class EvisionLightView
{
public:
	~EvisionLightView();
	static EvisionLightView * EvisionLightViewFactory();
	void show_windows();

	ImVec4 getWindowColor();


	void DrawDemoWindow();
	void HideDemoWindow();

	void DrawSettingWindow();
	void HideSettingWindow();

private:
	EvisionLightView();
	ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);
	//开关
	bool show_demo_window = false;
	bool show_Setting_window = false;

	//窗口定义和消息分发
	void DemoWindow();
	void SettingWindow();
	void ShowAppMainMenuBar();

	bool ImageButtonWithText(ImTextureID texId, const char* label, 
		const ImVec2& imageSize, const ImVec2& uv0, const ImVec2& uv1, 
		int frame_padding, const ImVec4& bg_col, const ImVec4& tint_col);
};
static EvisionLightView * m_pInstance;
