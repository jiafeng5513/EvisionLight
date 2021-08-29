// Dear ImGui: standalone example application for GLFW + OpenGL 3, using programmable pipeline
// (GLFW is a cross-platform general purpose library for handling windows, inputs, OpenGL/Vulkan/Metal graphics context creation, etc.)
// If you are new to Dear ImGui, read documentation from the docs/ folder + read the top of imgui.cpp.
// Read online: https://github.com/ocornut/imgui/tree/master/docs

#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include <stdio.h>

// About Desktop OpenGL function loaders:
//  Modern desktop OpenGL doesn't have a standard portable header file to load OpenGL function pointers.
//  Helper libraries are often used for this purpose! Here we are supporting a few common ones (gl3w, glew, glad).
//  You may use another loader/header of your choice (glext, glLoadGen, etc.), or chose to manually implement your own.
#if defined(IMGUI_IMPL_OPENGL_LOADER_GL3W)
#include <GL/gl3w.h>            // Initialize with gl3wInit()
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLEW)
#include <GL/glew.h>            // Initialize with glewInit()
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLAD)
#include <glad/glad.h>          // Initialize with gladLoadGL()
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLAD2)
#include <glad/gl.h>            // Initialize with gladLoadGL(...) or gladLoaderLoadGL()
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLBINDING2)
#define GLFW_INCLUDE_NONE       // GLFW including OpenGL headers causes ambiguity or multiple definition errors.
#include <glbinding/Binding.h>  // Initialize with glbinding::Binding::initialize()
#include <glbinding/gl/gl.h>
using namespace gl;
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLBINDING3)
#define GLFW_INCLUDE_NONE       // GLFW including OpenGL headers causes ambiguity or multiple definition errors.
#include <glbinding/glbinding.h>// Initialize with glbinding::initialize()
#include <glbinding/gl/gl.h>
using namespace gl;
#else
#include IMGUI_IMPL_OPENGL_LOADER_CUSTOM
#endif

// Include glfw3.h after our OpenGL definitions
#include <GLFW/glfw3.h>

#include <EvisionLightView.h>
#include "opencv2/opencv.hpp"
#include "boost/thread.hpp"
#include "boost/signals2.hpp"
#include "Observer.h"
#include "Observable.h"
#include "nfd.h"
#include "imageutils.h"

// [Win32] Our example includes a copy of glfw3.lib pre-compiled with VS2010 to maximize ease of testing and compatibility with old VS compilers.
// To link with VS2010-era libraries, VS2015+ requires linking with legacy_stdio_definitions.lib, which we do using this pragma.
// Your own project should not be affected, as you are likely to link with a newer binary of GLFW that is adequate for your version of Visual Studio.
#if defined(_MSC_VER) && (_MSC_VER >= 1900) && !defined(IMGUI_DISABLE_WIN32_FUNCTIONS)
#pragma comment(lib, "legacy_stdio_definitions")
#endif

static OpenCVImage gl_img;
cv::VideoCapture cap;

static void showImage(const char* windowName, bool* open, OpenCVImage& image)
{
    if (!image.isEmpty())
    {

        if (ImGui::Begin(windowName, open))
        {
            ImVec2 pos = ImGui::GetCursorScreenPos(); // actual position
            ImGui::GetWindowDrawList()->AddImage((void*)image.getTexture(), pos, ImVec2(ImGui::GetContentRegionAvail().x + pos.x, ImGui::GetContentRegionAvail().y + pos.y));
        }
        ImGui::End();
    }
}

void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
    {
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    }
}

void glfw_error_callback(int error, const char* description)
{
    fprintf(stderr, "Glfw Error %d: %s\n", error, description);
}

//static void glfw_error_callback(int error, const char* description)
//{
//    fprintf(stderr, "Glfw Error %d: %s\n", error, description);
//}

struct MainWindowObservers
{
    enum {
        OnButtonPressEvent,
        OnRunEvent,
        OnWorkerEvent,
        OnCloseEvent
    };
    using ObserverTable = std::tuple<
        Observer<void(std::string buttonName)>,
        Observer<void(void)>,
        Observer<void(void)>,
        Observer<void(void)>
    >;
};
class MainWindow : public Observable< MainWindowObservers>
{
public:
    std::string LocaleName;
    int width;
    int height;
    int sidePanelWidth;
    // Main window
    GLFWwindow* window;

    bool isRunning;
    std::mutex m;
    boost::thread* thr;

    MainWindow()
    {
        LocaleName = "ru_RU.utf8";
        setlocale(LC_ALL, LocaleName.c_str());
        // Size of window
        width = 1024;
        height = 768;
        // Width of side panel
        sidePanelWidth = 300;
        // Main window
        window = nullptr;

        isRunning = false;
        thr = nullptr;
    }

    ~MainWindow()
    {
        if (thr != nullptr)
        {
            thr->interrupt();
            thr->join();
            delete thr;
            thr = nullptr;
        }
    }
    void InitGraphics()
    {
        // Setup window
        glfwSetErrorCallback(glfw_error_callback);
        if (!glfwInit())
        {
            return;
        }
        // Decide GL+GLSL versions
#if __APPLE__
    // GL 3.2 + GLSL 150
        const char* glsl_version = "#version 150";
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // 3.2+ only
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);            // Required on Mac
#else
    // GL 3.0 + GLSL 130
        const char* glsl_version = "#version 130";
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
        //glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // 3.2+ only
        //glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);            // 3.0+ only
#endif

    // Create window with graphics context
        window = glfwCreateWindow(width, height, "Tracker Generator", NULL, NULL);
        if (window == NULL)
            return;
        glfwSetKeyCallback(window, key_callback);
        glfwMakeContextCurrent(window);
        glfwSwapInterval(1); // Enable vsync
        // Initialize OpenGL loader
#if defined(IMGUI_IMPL_OPENGL_LOADER_GL3W)
        bool err = gl3wInit() != 0;
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLEW)
        bool err = glewInit() != GLEW_OK;
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLAD)
        bool err = gladLoadGL() == 0;
#else
        bool err = false; // If you use IMGUI_IMPL_OPENGL_LOADER_CUSTOM, your loader is likely to requires some form of initialization.
#endif
        if (err)
        {
            fprintf(stderr, "Failed to initialize OpenGL loader!\n");
            return;
        }
        // Setup Dear ImGui context
        IMGUI_CHECKVERSION();
        ImGui::CreateContext();
        ImGuiIO& io = ImGui::GetIO(); (void)io;
        // Setup Platform/Renderer bindings
        ImGui_ImplGlfw_InitForOpenGL(window, true);
        ImGui_ImplOpenGL3_Init(glsl_version);
        // Load Fonts
        //io.Fonts->AddFontFromFileTTF("fonts/a_FuturaOrto.TTF", 20, NULL, io.Fonts->GetGlyphRangesCyrillic());
        io.Fonts->AddFontFromFileTTF("F:/VisualStudio/EvisionLight/fonts/SourceHanSans.ttc",
            22.0f, NULL, io.Fonts->GetGlyphRangesChineseFull());
    }

    // -----------------------------
    // Free graphic resources
    // -----------------------------
    void TerminateGraphics(void)
    {
        // Cleanup
        ImGui_ImplOpenGL3_Shutdown();
        ImGui_ImplGlfw_Shutdown();
        ImGui::DestroyContext();
        glfwDestroyWindow(window);
        glfwTerminate();
    }
    // -----------------------------
    // Main loop
    // -----------------------------
    void worker(void)
    {
        isRunning = true;
        bool show_img_window = true;
        InitGraphics();
        Notify<MainWindowObservers::OnRunEvent>();
        EvisionLightView* view = EvisionLightView::EvisionLightViewFactory();
        // -------------
        // Main loop
        // -------------
        while (!boost::this_thread::interruption_requested() && !glfwWindowShouldClose(window))
        {
            // Poll and handle events (inputs, window resize, etc.)
            // You can read the io.WantCaptureMouse, io.WantCaptureKeyboard flags to tell if dear imgui wants to use your inputs.
            // - When io.WantCaptureMouse is true, do not dispatch mouse input data to your main application.
            // - When io.WantCaptureKeyboard is true, do not dispatch keyboard input data to your main application.
            // Generally you may always pass all inputs to dear imgui, and hide them from your application based on those two flags.
            
            glfwPollEvents();
            // Start the Dear ImGui frame
            ImGui_ImplOpenGL3_NewFrame();
            ImGui_ImplGlfw_NewFrame();
            ImGui::NewFrame();

            
            //ImGui::SetNextWindowSize(ImVec2(sidePanelWidth, height));
            //ImGui::SetNextWindowPos(ImVec2(0, 0));
            ImGui::Begin("image loader", &show_img_window);
            //ImGui::Begin("Panel", nullptr, ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoDecoration);
            if (ImGui::Button("Load image", ImVec2(-1, 0)))
            {
                Notify<MainWindowObservers::OnButtonPressEvent>("Load image");
            }
            if (ImGui::Button("Open video", ImVec2(-1, 0)))
            {
                Notify<MainWindowObservers::OnButtonPressEvent>("Open video");
            }
            ImGui::End();
            view->show_windows();

            Notify<MainWindowObservers::OnWorkerEvent>();
            glClearColor(0, 0, 0, 1.0);
            glClear(GL_COLOR_BUFFER_BIT);
            //ImGui::End();


            // Rendering
            ImGui::Render();
            ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
            glfwSwapBuffers(window);
        }
        TerminateGraphics();
        isRunning = false;
        Notify<MainWindowObservers::OnCloseEvent>();
    }
    void Run(void)
    {
        if (!isRunning)
        {
            thr = new boost::thread(&MainWindow::worker, this);
            isRunning = true;
        }
    }

    void Stop(void)
    {
        if (isRunning)
        {
            thr->interrupt();
            thr->join();
            delete thr;
            thr = nullptr;
            isRunning = false;
        }
    }

};

class Application
{
public:
    // -----------------------------
    //
    // -----------------------------
    explicit Application(MainWindow& worker) :
        worker_(worker)
    {
        finished = false;

        worker_.Register < MainWindowObservers::OnCloseEvent >([this](void)
            {
                OnClose();
            });

        worker_.Register < MainWindowObservers::OnRunEvent >([this](void)
            {
                OnRun();
            });
        worker_.Register < MainWindowObservers::OnWorkerEvent >([this](void)
            {
                OnShowImage();
            });
        worker_.Register < MainWindowObservers::OnButtonPressEvent >([this](std::string button_name)
            {
                OnButton(button_name);
            });
        std::cout << "Events - registered" << std::endl;

        worker_.Run();

        while (worker_.isRunning)
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(100));
            finished = true;
        }
        worker_.Stop();
    }
    // -----------------------------
    //
    // -----------------------------
    ~Application()
    {

    }

private:
    bool finished;

    void OnRun()
    {
        std::cout << "On run event." << std::endl;
    }

    void OnClose()
    {
        std::cout << "On close event." << std::endl;
    }

    void OnShowImage()
    {
        if (cap.isOpened())
        {
            cv::Mat img;
            cap >> img;
            if (!img.empty())
            {
                gl_img.SetMat(img, true);
            }
            else
            {
                cap.release();
            }
        }

        static bool p_open = true;
        ImGui::SetNextWindowSize(ImVec2(gl_img.GetMat().cols, gl_img.GetMat().rows));
        showImage("image", &p_open, gl_img);
    }



    void OnButton(std::string button_name)
    {
        if (button_name == "Load image")
        {
            nfdchar_t* outPath = NULL;
            nfdresult_t result = NFD_OpenDialog("jpg", NULL, &outPath);
            if (result == NFD_OKAY)
            {
                cv::Mat img = cv::imread(outPath);
                gl_img.SetMat(img, true);
                free(outPath);
            }
            else if (result == NFD_CANCEL)
            {
                std::cout << "User pressed cancel." << std::endl;
            }
            else
            {
                std::cout << "Error: " << NFD_GetError() << std::endl;
            }
        }

        if (button_name == "Open video")
        {
            nfdchar_t* outPath = NULL;
            nfdresult_t result = NFD_OpenDialog("avi", NULL, &outPath);
            if (result == NFD_OKAY)
            {
                cap.open(outPath);
                free(outPath);
            }
            else if (result == NFD_CANCEL)
            {
                std::cout << "User pressed cancel." << std::endl;
            }
            else
            {
                std::cout << "Error: " << NFD_GetError() << std::endl;
            }
        }

    }
    MainWindow& worker_;
};


int main()
{
    MainWindow worker;
    Application application{ worker };
}

int main1(int, char**)
{
    // Setup window
    glfwSetErrorCallback(glfw_error_callback);
    if (!glfwInit())
        return 1;

    // Decide GL+GLSL versions
#ifdef __APPLE__
    // GL 3.2 + GLSL 150
    const char* glsl_version = "#version 150";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // 3.2+ only
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);            // Required on Mac
#else
    // GL 3.0 + GLSL 130
    const char* glsl_version = "#version 130";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);
    //glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);  // 3.2+ only
    //glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);            // 3.0+ only
#endif

    // Create window with graphics context
    GLFWwindow* window = glfwCreateWindow(1280, 720, "Dear ImGui GLFW+OpenGL3 example", NULL, NULL);
    if (window == NULL)
        return 1;
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1); // Enable vsync

    // Initialize OpenGL loader
#if defined(IMGUI_IMPL_OPENGL_LOADER_GL3W)
    bool err = gl3wInit() != 0;
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLEW)
    bool err = glewInit() != GLEW_OK;
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLAD)
    bool err = gladLoadGL() == 0;
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLAD2)
    bool err = gladLoadGL(glfwGetProcAddress) == 0; // glad2 recommend using the windowing library loader instead of the (optionally) bundled one.
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLBINDING2)
    bool err = false;
    glbinding::Binding::initialize();
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLBINDING3)
    bool err = false;
    glbinding::initialize([](const char* name) { return (glbinding::ProcAddress)glfwGetProcAddress(name); });
#else
    bool err = false; // If you use IMGUI_IMPL_OPENGL_LOADER_CUSTOM, your loader is likely to requires some form of initialization.
#endif
    if (err)
    {
        fprintf(stderr, "Failed to initialize OpenGL loader!\n");
        return 1;
    }

    // Setup Dear ImGui context
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;       // Enable Keyboard Controls
    //io.ConfigFlags |= ImGuiConfigFlags_NavEnableGamepad;      // Enable Gamepad Controls
    io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;           // Enable Docking
    io.ConfigFlags |= ImGuiConfigFlags_ViewportsEnable;         // Enable Multi-Viewport / Platform Windows
    //io.ConfigViewportsNoAutoMerge = true;
    //io.ConfigViewportsNoTaskBarIcon = true;

    // Setup Dear ImGui style
    ImGui::StyleColorsDark();
    //ImGui::StyleColorsClassic();

    // When viewports are enabled we tweak WindowRounding/WindowBg so platform windows can look identical to regular ones.
    ImGuiStyle& style = ImGui::GetStyle();
    if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable)
    {
        style.WindowRounding = 0.0f;
        style.Colors[ImGuiCol_WindowBg].w = 1.0f;
    }

    // Setup Platform/Renderer backends
    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);

    // Load Fonts
    // - If no fonts are loaded, dear imgui will use the default font. You can also load multiple fonts and use ImGui::PushFont()/PopFont() to select them.
    // - AddFontFromFileTTF() will return the ImFont* so you can store it if you need to select the font among multiple.
    // - If the file cannot be loaded, the function will return NULL. Please handle those errors in your application (e.g. use an assertion, or display an error and quit).
    // - The fonts will be rasterized at a given size (w/ oversampling) and stored into a texture when calling ImFontAtlas::Build()/GetTexDataAsXXXX(), which ImGui_ImplXXXX_NewFrame below will call.
    // - Read 'docs/FONTS.md' for more instructions and details.
    // - Remember that in C/C++ if you want to include a backslash \ in a string literal you need to write a double backslash \\ !
    //io.Fonts->AddFontDefault();
    //io.Fonts->AddFontFromFileTTF("../../misc/fonts/Roboto-Medium.ttf", 16.0f);
    //io.Fonts->AddFontFromFileTTF("../../misc/fonts/Cousine-Regular.ttf", 15.0f);
    //io.Fonts->AddFontFromFileTTF("../../misc/fonts/DroidSans.ttf", 16.0f);
    //io.Fonts->AddFontFromFileTTF("../../misc/fonts/ProggyTiny.ttf", 10.0f);
    //ImFont* font = io.Fonts->AddFontFromFileTTF("c:\\Windows\\Fonts\\ArialUni.ttf", 18.0f, NULL, io.Fonts->GetGlyphRangesJapanese());
    //IM_ASSERT(font != NULL);
    ImFont* font = io.Fonts->AddFontFromFileTTF("E:/VisualStudio/imgui_opencv_template/fonts/SourceHanSans.ttc",
        22.0f, NULL, io.Fonts->GetGlyphRangesChineseFull());

    // Our state
    bool show_demo_window = true;
    bool show_another_window = false;
    ImVec4 clear_color = ImVec4(0.45f, 0.55f, 0.60f, 1.00f);

    EvisionLightView* view = EvisionLightView::EvisionLightViewFactory();

    // Main loop
    while (!glfwWindowShouldClose(window))
    {
        // Poll and handle events (inputs, window resize, etc.)
        // You can read the io.WantCaptureMouse, io.WantCaptureKeyboard flags to tell if dear imgui wants to use your inputs.
        // - When io.WantCaptureMouse is true, do not dispatch mouse input data to your main application.
        // - When io.WantCaptureKeyboard is true, do not dispatch keyboard input data to your main application.
        // Generally you may always pass all inputs to dear imgui, and hide them from your application based on those two flags.
        glfwPollEvents();

        // Start the Dear ImGui frame
        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        view->show_windows();

        // 1. Show the big demo window (Most of the sample code is in ImGui::ShowDemoWindow()! You can browse its code to learn more about Dear ImGui!).
        if (show_demo_window)
            ImGui::ShowDemoWindow(&show_demo_window);

        // 2. Show a simple window that we create ourselves. We use a Begin/End pair to created a named window.
        {
            static float f = 0.0f;
            static int counter = 0;

            ImGui::Begin("Hello, world!");                          // Create a window called "Hello, world!" and append into it.

            ImGui::Text("This is some useful text.");               // Display some text (you can use a format strings too)
            ImGui::Checkbox("Demo Window", &show_demo_window);      // Edit bools storing our window open/close state
            ImGui::Checkbox("Another Window", &show_another_window);

            ImGui::SliderFloat("float", &f, 0.0f, 1.0f);            // Edit 1 float using a slider from 0.0f to 1.0f
            ImGui::ColorEdit3("clear color", (float*)&clear_color); // Edit 3 floats representing a color

            if (ImGui::Button("Button"))                            // Buttons return true when clicked (most widgets return true when edited/activated)
                counter++;
            ImGui::SameLine();
            ImGui::Text("counter = %d", counter);

            ImGui::Text("Application average %.3f ms/frame (%.1f FPS)", 1000.0f / ImGui::GetIO().Framerate, ImGui::GetIO().Framerate);
            ImGui::End();
        }

        // 3. Show another simple window.
        if (show_another_window)
        {
            ImGui::Begin("Another Window", &show_another_window);   // Pass a pointer to our bool variable (the window will have a closing button that will clear the bool when clicked)
            ImGui::Text("Hello from another window!");
            if (ImGui::Button("Close Me"))
                show_another_window = false;
            ImGui::End();
        }

        // Rendering
        ImGui::Render();
        int display_w, display_h;
        glfwGetFramebufferSize(window, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);
        glClearColor(clear_color.x, clear_color.y, clear_color.z, clear_color.w);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
    	
        // Update and Render additional Platform Windows
        // (Platform functions may change the current OpenGL context, so we save/restore it to make it easier to paste this code elsewhere.
        //  For this specific demo app we could also call glfwMakeContextCurrent(window) directly)
        if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable)
        {
            GLFWwindow* backup_current_context = glfwGetCurrentContext();
            ImGui::UpdatePlatformWindows();
            ImGui::RenderPlatformWindowsDefault();
            glfwMakeContextCurrent(backup_current_context);
        }

        glfwSwapBuffers(window);
    }

    // Cleanup
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();

    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}
