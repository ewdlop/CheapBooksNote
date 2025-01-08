using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace VacuumPackaging
{
    // 包裝材料類型
    public enum PackagingMaterial
    {
        PA_PE,          // 尼龍/聚乙烯複合膜
        PET_PE,         // PET/聚乙烯複合膜
        PVDC,           // 聚偏二氯乙烯
        AL_PE,          // 鋁箔/聚乙烯複合膜
        HighBarrier     // 高阻隔膜
    }

    // 真空程度等級
    public enum VacuumLevel
    {
        Light = 80,     // 輕度真空 (80% 真空度)
        Medium = 90,    // 中度真空 (90% 真空度)
        High = 95,      // 高度真空 (95% 真空度)
        Ultra = 99      // 超高真空 (99% 真空度)
    }

    // 包裝產品資訊
    public class Product
    {
        public string Name { get; set; }
        public double Weight { get; set; }
        public double Moisture { get; set; }
        public bool RequiresRefrigeration { get; set; }
        public DateTime PackagingDate { get; set; }
        public DateTime ExpiryDate { get; set; }
    }

    // 包裝設定
    public class PackagingSettings
    {
        public PackagingMaterial Material { get; set; }
        public VacuumLevel VacuumLevel { get; set; }
        public double SealingTemperature { get; set; }
        public int SealingTime { get; set; }
        public bool UseNitrogenFlushing { get; set; }
    }

    // 真空包裝機控制器
    public class VacuumPackagingMachine
    {
        private bool _isRunning;
        private readonly Dictionary<PackagingMaterial, double> _materialThickness;

        public VacuumPackagingMachine()
        {
            _materialThickness = new Dictionary<PackagingMaterial, double>
            {
                { PackagingMaterial.PA_PE, 0.09 },
                { PackagingMaterial.PET_PE, 0.12 },
                { PackagingMaterial.PVDC, 0.08 },
                { PackagingMaterial.AL_PE, 0.15 },
                { PackagingMaterial.HighBarrier, 0.18 }
            };
        }

        // 檢查包裝設定是否合適
        public bool ValidateSettings(Product product, PackagingSettings settings)
        {
            // 檢查封口溫度是否在安全範圍內
            if (settings.SealingTemperature < 120 || settings.SealingTemperature > 180)
                return false;

            // 檢查真空度是否適合產品水分含量
            if (product.Moisture > 80 && settings.VacuumLevel == VacuumLevel.Ultra)
                return false;

            // 檢查材料是否適合需要冷藏的產品
            if (product.RequiresRefrigeration && 
                !(settings.Material == PackagingMaterial.HighBarrier || 
                  settings.Material == PackagingMaterial.AL_PE))
                return false;

            return true;
        }

        // 開始包裝流程
        public async Task<bool> StartPackaging(Product product, PackagingSettings settings)
        {
            if (!ValidateSettings(product, settings))
            {
                throw new InvalidOperationException("包裝設定不符合產品要求");
            }

            _isRunning = true;
            try
            {
                // 1. 預熱封口系統
                await PreHeatSealer(settings.SealingTemperature);

                // 2. 抽真空
                await CreateVacuum(settings.VacuumLevel);

                // 3. 氮氣填充 (如果需要)
                if (settings.UseNitrogenFlushing)
                {
                    await FlushNitrogen();
                }

                // 4. 熱封口
                await SealPackage(settings);

                // 5. 冷卻
                await CoolDown();

                return true;
            }
            catch (Exception)
            {
                return false;
            }
            finally
            {
                _isRunning = false;
            }
        }

        // 預熱封口系統
        private async Task PreHeatSealer(double temperature)
        {
            Console.WriteLine($"預熱封口系統至 {temperature}°C");
            await Task.Delay(2000); // 模擬預熱時間
        }

        // 抽真空過程
        private async Task CreateVacuum(VacuumLevel level)
        {
            int percentage = (int)level;
            Console.WriteLine($"正在抽真空至 {percentage}%");
            await Task.Delay(3000); // 模擬抽真空時間
        }

        // 氮氣填充
        private async Task FlushNitrogen()
        {
            Console.WriteLine("進行氮氣填充");
            await Task.Delay(1500); // 模擬填充時間
        }

        // 熱封口
        private async Task SealPackage(PackagingSettings settings)
        {
            Console.WriteLine($"使用 {settings.SealingTemperature}°C 進行熱封口");
            await Task.Delay(settings.SealingTime); // 實際封口時間
        }

        // 冷卻過程
        private async Task CoolDown()
        {
            Console.WriteLine("進行冷卻");
            await Task.Delay(2000); // 模擬冷卻時間
        }

        // 取得包裝狀態
        public bool IsRunning => _isRunning;

        // 計算建議的封口時間
        public int CalculateRecommendedSealingTime(PackagingMaterial material)
        {
            double thickness = _materialThickness[material];
            return (int)(thickness * 1000); // 根據材料厚度計算建議時間
        }
    }

    // 使用範例
    public class Program
    {
        public static async Task Main()
        {
            var machine = new VacuumPackagingMachine();

            var product = new Product
            {
                Name = "冷凍魚片",
                Weight = 500,
                Moisture = 75,
                RequiresRefrigeration = true,
                PackagingDate = DateTime.Now,
                ExpiryDate = DateTime.Now.AddDays(90)
            };

            var settings = new PackagingSettings
            {
                Material = PackagingMaterial.HighBarrier,
                VacuumLevel = VacuumLevel.High,
                SealingTemperature = 150,
                SealingTime = 1200,
                UseNitrogenFlushing = true
            };

            try
            {
                bool result = await machine.StartPackaging(product, settings);
                if (result)
                {
                    Console.WriteLine("包裝完成");
                }
                else
                {
                    Console.WriteLine("包裝失敗");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"錯誤: {ex.Message}");
            }
        }
    }
}
