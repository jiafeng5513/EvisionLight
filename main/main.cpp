#include <iostream>
#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include "boost/thread.hpp"
#include "boost/signals2.hpp"
#include "Observer.h"
#include "Observable.h"
#include "nfd.h"

// About OpenGL function loaders: modern OpenGL doesn't have a standard header file and requires individual function pointers to be loaded manually.
// Helper libraries are often used for this purpose! Here we are supporting a few common ones: gl3w, glew, glad.
// You may use another loader/header of your choice (glext, glLoadGen, etc.), or chose to manually implement your own.
#if defined(IMGUI_IMPL_OPENGL_LOADER_GL3W)
#include <GL/gl3w.h>    // Initialize with gl3wInit()
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLEW)
#include <GL/glew.h>    // Initialize with glewInit()
#elif defined(IMGUI_IMPL_OPENGL_LOADER_GLAD)
#include <glad/glad.h>  // Initialize with gladLoadGL()
#else
#include IMGUI_IMPL_OPENGL_LOADER_CUSTOM
#endif

// Include glfw3.h after our OpenGL definitions
#include <GLFW/glfw3.h>
// [Win32] Our example includes a copy of glfw3.lib pre-compiled with VS2010 to maximize ease of testing and compatibility with old VS compilers.
// To link with VS2010-era libraries, VS2015+ requires linking with legacy_stdio_definitions.lib, which we do using this pragma.
// Your own project should not be affected, as you are likely to link with a newer binary of GLFW that is adequate for your version of Visual Studio.
#if defined(_MSC_VER) && (_MSC_VER >= 1900) && !defined(IMGUI_DISABLE_WIN32_FUNCTIONS)
#pragma comment(lib, "legacy_stdio_definitions")
#endif

#include<opencv2/opencv.hpp>
#include "imageutils.h"

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
// -----------------------------
//
// -----------------------------
void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
    {
        glfwSetWindowShouldClose(window, GLFW_TRUE);
    }
}
// -----------------------------
//
// -----------------------------
void glfw_error_callback(int error, const char* description)
{
    fprintf(stderr, "Glfw Error %d: %s\n", error, description);
}
// -----------------------------
//
// -----------------------------
struct MainWindowObservers
{
    enum { OnButtonPressEvent,
           OnRunEvent,
           OnWorkerEvent,
           OnCloseEvent };
    using ObserverTable = std::tuple<
        Observer<void(std::string buttonName)>,
        Observer<void(void)>,
        Observer<void(void)>,
        Observer<void(void)>
    >;
};
// -----------------------------
//
// -----------------------------
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
        io.Fonts->AddFontFromFileTTF("fonts/a_FuturaOrto.TTF", 20, NULL, io.Fonts->GetGlyphRangesCyrillic());
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
        InitGraphics();
        Notify<MainWindowObservers::OnRunEvent>();
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

            ImGui::SetNextWindowSize(ImVec2(sidePanelWidth, height));
            ImGui::SetNextWindowPos(ImVec2(0, 0));
                                    
            ImGui::Begin("Panel", nullptr, ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoDecoration);               
            if (ImGui::Button("Load image",ImVec2(-1,0)))
            {
                Notify<MainWindowObservers::OnButtonPressEvent>("Load image");
            }
            if (ImGui::Button("Open video", ImVec2(-1, 0)))
            {
                Notify<MainWindowObservers::OnButtonPressEvent>("Open video");
            }
            ImGui::End();

            Notify<MainWindowObservers::OnWorkerEvent>();
 
            glClearColor(0, 0, 0, 1.0);
            glClear(GL_COLOR_BUFFER_BIT);
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

// -----------------------------
//
// -----------------------------
// Application: our Observer.
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
                OnWorker();
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

    void OnWorker()
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

// -----------------------------
//
// -----------------------------
int main()
{
    MainWindow worker;  
    Application application{ worker };
}

