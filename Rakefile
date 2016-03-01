namespace :csv do

  file "dfec-volume-fraction-775.csv" => "dfec_volume_fraction.py" do |f|
    sh "python #{f.prerequisites[0]} --diameter 7.75e-6 --output #{f.name}"
  end

  file "dfec-volume-fraction-185.csv" => "dfec_volume_fraction.py" do |f|
    sh "python #{f.prerequisites[0]} --diameter 1.85e-6 --output #{f.name}"
  end

  task :all => [
    "dfec-volume-fraction-775.csv",
    "dfec-volume-fraction-185.csv",
  ]

end

namespace :ggplot do

  file "dfec-volume-fraction-185.png" => ["plot_dfec_volume_fraction.R", "dfec-volume-fraction-185.csv"] do |f|
    sh "./#{f.prerequisites.join(" ")} #{f.name}"
  end

  file "dfec-volume-fraction-775.png" => ["plot_dfec_volume_fraction.R", "dfec-volume-fraction-775.csv"] do |f|
    sh "./#{f.prerequisites.join(" ")} #{f.name}"
  end

  task :all => [
    "dfec-volume-fraction-775.png",
    "dfec-volume-fraction-185.png",
  ]

end

task :default => [
  "csv:all",
  "ggplot:all",
]
