<?php

include_once __DIR__ . '/../vendor/autoload.php';
include_once __DIR__ . '/Factories/HttpClientFactory.php';
include_once __DIR__ . '/Parsers/SiteMapParser.php';

use TingChina\Factories\HttpClientFactory;
use TingChina\Parsers\SiteMapParser;

class main
{
    const SITE_MAP_URI = 'yousheng/sitemap.htm';

    private $httpClient;

    private $siteMapParser;

    private $downloading = [];

    public function __construct()
    {
        $this->httpClient = HttpClientFactory::get();
        $this->siteMapParser = new SiteMapParser();
    }

    public function __invoke()
    {
        ini_set('implicit_flush', true);
        ob_implicit_flush(true);

        $books = ($this->siteMapParser)($this->httpClient, self::SITE_MAP_URI);
        foreach ($books as $id => $title) {
            echo (new DateTimeImmutable())->format(DateTimeImmutable::RFC3339);
            echo " Book $id: $title" . PHP_EOL;
            flush();
            $this->downloadBook($id, $title);
        }
    }

    private function downloadBook($id, string $title)
    {
        echo "start downloading $id: $title" . PHP_EOL;

        $basePath = '/mnt/v/AudioBooks';
        $path = $basePath . "/$title";
        if (!file_exists($path)) {
            mkdir($path, 0777, true);
        }
        $cmd = 'python3 ' . __DIR__ . "/../My_yousheng.py $id $path";
        $this->downloading[$id] = $title;

        $cpuLimit = $this->get_processor_cores_number();
        while (sys_getloadavg()[0] > $cpuLimit || sys_getloadavg()[1] > $cpuLimit) {
            echo 'CPU load too high ' . implode(',', sys_getloadavg()) . PHP_EOL;
            sleep(10);
        }

        echo "CMD: $cmd" . PHP_EOL;

        $outputfile = __DIR__ . '/../dist/' . $id . '.log';
        $pidfile = __DIR__ . '/../dist/' . $id . '.pid';
        exec(sprintf("%s > %s 2>&1 & echo $! >> %s", $cmd, $outputfile, $pidfile));

        $this->downloading[] = $outputfile;
    }

    private function get_processor_cores_number()
    {
        $command = "cat /proc/cpuinfo | grep processor | wc -l";

        return (int)shell_exec($command);
    }
}

(new Main())();
