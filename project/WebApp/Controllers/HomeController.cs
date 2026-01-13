using Microsoft.AspNetCore.Mvc;
using StackExchange.Redis;
using WebApp.Models;
using System.Text.Json;

namespace WebApp.Controllers;

public class HomeController : Controller
{
    private static ConnectionMultiplexer _redis = ConnectionMultiplexer.Connect("localhost");

    public async Task<IActionResult> Index()
    {
        try {
            using (var client = new HttpClient()) {
                client.DefaultRequestHeaders.UserAgent.ParseAdd("Mozilla/5.0");
                ViewBag.Weather = await client.GetStringAsync("https://wttr.in/Sofia?format=3");
            }
        } catch { ViewBag.Weather = "Weather service unavailable"; }

        var uploadDir = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "uploads");
        if (Directory.Exists(uploadDir))
        {
            var files = Directory.GetFiles(uploadDir, "processed_*.*")
                                 .Select(f => Path.GetFileName(f))
                                 .OrderByDescending(f => f)
                                 .ToList();
            ViewBag.Images = files;
        }
        else
        {
            ViewBag.Images = new List<string>();
        }

        return View("Index");
    }

    public IActionResult Privacy()
    {
        return View();
    }

    [HttpPost]
    public async Task<IActionResult> UploadImage(IFormFile file, string rotation, string effect, string watermarkText)
    {
        if (file != null && file.Length > 0)
        {
            var uploadDir = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "uploads");
            if (!Directory.Exists(uploadDir)) Directory.CreateDirectory(uploadDir);

            var fileName = Guid.NewGuid().ToString() + Path.GetExtension(file.FileName);
            var fullPath = Path.Combine(uploadDir, fileName);

            using (var stream = new FileStream(fullPath, FileMode.Create))
            {
                await file.CopyToAsync(stream);
            }

            // Пращаме всички параметри поотделно
            var taskData = new 
            { 
                Path = fullPath, 
                Rotation = rotation ?? "none",
                Effect = effect ?? "none",
                Watermark = watermarkText ?? ""
            };
            
            string jsonMessage = JsonSerializer.Serialize(taskData);

            var db = _redis.GetDatabase();
            await db.ListLeftPushAsync("image_queue", jsonMessage);

            ViewBag.Message = "Снимката е изпратена за комбинирана обработка!";
        }
        
        return await Index(); 
    }

    [HttpGet]
    public IActionResult GetProcessedImages()
    {
        var uploadDir = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "uploads");
        if (!Directory.Exists(uploadDir)) return Json(new List<string>());

        var files = Directory.GetFiles(uploadDir, "processed_*.*")
                             .Select(f => Path.GetFileName(f))
                             .OrderByDescending(f => f)
                             .ToList();

        return Json(files);
    }
}