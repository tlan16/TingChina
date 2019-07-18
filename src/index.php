<?php

include_once __DIR__.'/../vendor/autoload.php';
include_once __DIR__.'/Factories/HttpClientFactory.php';
include_once __DIR__.'/Parsers/SiteMapParser.php';

use TingChina\Factories\HttpClientFactory;
use TingChina\Parsers\SiteMapParser;

class main
{
    const SITE_MAP_URI = 'yousheng/sitemap.htm';

    private $httpClient;

    private $siteMapParser;

    public function __construct()
    {
        $this->httpClient = HttpClientFactory::get();
        $this->siteMapParser = new SiteMapParser();
    }

    public function __invoke()
    {
        $books = ($this->siteMapParser)($this->httpClient, self::SITE_MAP_URI);
        foreach ($books as $id => $title) {
            $this->downloadBook($id, $title);
        }
    }

    private function downloadBook($id, string $title)
    {
        $this->disable_ob();

        $path = __DIR__."/../dist/$title";
        mkdir($path, 0777, true);
        $cmd = 'python3 '.__DIR__."/../My_yousheng.py $id $path";
        system($cmd);
    }

    private function disable_ob() {
        // Turn off output buffering
        ini_set('output_buffering', 'off');
        // Turn off PHP output compression
        ini_set('zlib.output_compression', false);
        // Implicitly flush the buffer(s)
        ini_set('implicit_flush', true);
        ob_implicit_flush(true);
        // Clear, and turn off output buffering
        while (ob_get_level() > 0) {
            // Get the curent level
            $level = ob_get_level();
            // End the buffering
            ob_end_clean();
            // If the current level has not changed, abort
            if (ob_get_level() == $level) break;
        }
        // Disable apache output buffering/compression
        if (function_exists('apache_setenv')) {
            apache_setenv('no-gzip', '1');
            apache_setenv('dont-vary', '1');
        }
    }
}

(new Main())();
