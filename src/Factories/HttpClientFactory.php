<?php

namespace TingChina\Factories;

use GuzzleHttp\Client;
use GuzzleHttp\ClientInterface;

class HttpClientFactory
{
    public static function get(array $options = []): ClientInterface
    {
        $defaultOptions = [
            'base_uri' => 'http://www.tingchina.com/',
        ];
        $mergedOptions = array_merge($defaultOptions, $options);

        $client = new Client($mergedOptions);

        return $client;
    }
}
