
#include "opencv2/opencv.hpp"
#include <GLFW/glfw3.h>
#include <string>
#include <sstream>
#include <iostream>

class OpenCVImage
{
public:
    OpenCVImage() 
    {
        texture = 0;
        open = true;
        name = "noname";
    }

    OpenCVImage(cv::Mat& frame, bool swap_RB = true)
    {
        Clear();
        SetMat(frame, swap_RB);
    }


    void SetMat(cv::Mat& frame, bool swap_RB = false) 
    {
        if (frame.empty())
        {
            return;
        }
        bool needUpdate = !(frame.size() == mat.size());
        if (swap_RB)
        {
            cv::cvtColor(frame, mat, cv::COLOR_BGR2RGBA);
        }
        else
        {
            cv::cvtColor(frame, mat, cv::COLOR_RGB2RGBA);
        }

        if (needUpdate)
        {
            Clear();
            glGenTextures(1, &texture);
            glBindTexture(GL_TEXTURE_2D, texture);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST);
            // Set texture clamping method
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER);
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, mat.cols, mat.rows, 0, GL_RGBA, GL_UNSIGNED_BYTE, mat.ptr());                
        }
        else
        {
            glBindTexture(GL_TEXTURE_2D, texture);
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, mat.cols, mat.rows, 0, GL_RGBA, GL_UNSIGNED_BYTE, mat.data);
        }
    }

    // clear texture and realease all memory associated with it
    void Clear(void) 
    {
        if (texture)
        {
            glDeleteTextures(1, &texture);
        }
        texture = 0; 
    }

    GLuint& getTexture(void) 
    {
        return texture; 
    }

    // return mat if is not empty otherwise return null
    void GetMat(cv::Mat& res)
    {
        res = mat;
    }

    cv::Mat& GetMat(void)
    {
        return mat;
    }
    void switchOpen(void) 
    {
        if (open)
        {
            open = false;
        }
        else
        {
            open = true;
        }
    }

    bool* getOpen() { return &open; }
    bool  isEmpty() { return mat.empty(); }
    void SetName(const char* nme) 
    {
        name = std::string(nme);
    }

    const char* GetName(void)
    {
        return name.c_str();
    }
    
private:
    GLuint texture;
    cv::Mat mat;
    bool open;
    std::string name;
};
