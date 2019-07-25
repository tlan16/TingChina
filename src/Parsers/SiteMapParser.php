<?php

namespace TingChina\Parsers;

include_once __DIR__.'/simple_html_dom.php';

use function array_map;
use function array_reduce;
use function file;
use function get_class;
use GuzzleHttp\ClientInterface;
use function iconv;
use function is_string;
use function mb_convert_encoding;
use function rtrim;
use function str_get_html;
use Symfony\Component\DomCrawler\Crawler;
use function var_dump;
use \ForceUTF8\Encoding;


class SiteMapParser
{
    public function __invoke(ClientInterface $client, string $uri)
    {
        $httpResponse = $client->request('GET', $uri);
        $html = (string) $httpResponse->getBody();
        file_put_contents('test.html', $html);

        $books = [];
        $re = '/(?<=<li>)<a href="\S+"\s+ title="\S+"\s*\S+(?=<\/li>)/m';
        preg_match_all($re, $html, $links, PREG_SET_ORDER, 0);
        foreach ($links as $link) {
            $link = $link[0];
            $id = $this->getIdFromLink($link);
            $title = $this->getTitleFromLink($link);
            $title = @iconv('gb2312', 'utf-8', $title);

            if (!is_string($title)) {
                continue;
            }

            $books[$id] = $title;
        }

        return $books;
    }

    private function getTitleFromLink(string $link):string {
        $re = '/(?<=>)\S+(?=<\/a>)/m';
        preg_match_all($re, $link, $matches, PREG_SET_ORDER, 0);

        return $matches[0][0];

    }

    private function getIdFromLink(string $link): string
    {
        $re = '/(?<=href="\/yousheng\/disp_)\d+/m';

        preg_match_all($re, $link, $matches, PREG_SET_ORDER, 0);

        return $matches[0][0];
    }
}
