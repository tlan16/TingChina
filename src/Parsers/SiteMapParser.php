<?php

namespace TingChina\Parsers;

include_once __DIR__.'/simple_html_dom.php';

use function array_map;
use function array_reduce;
use GuzzleHttp\ClientInterface;
use function str_get_html;

class SiteMapParser
{
    public function __invoke(ClientInterface $client, string $uri)
    {
        $httpResponse = $client->request('GET', $uri);
        $html = (string) $httpResponse->getBody();
        file_put_contents('test.html', $html);
        $html = str_get_html($html);

        $links = $html->find('.singerlist2 a');

        $books = array_reduce(
            $links,
            function (array $books, $link): array {
                $href = $link->href;
                $title = $link->title;
                $id = $this->getIdFromHref($href);

                $books[$id] = $title;
                return $books;
            },
            []
        );

        return $books;
    }

    private function getIdFromHref(string $href): string
    {
        $re = '/(?<=\/yousheng\/disp_)\d+/m';

        preg_match_all($re, $href, $matches, PREG_SET_ORDER, 0);

        return $matches[0][0];
    }
}
