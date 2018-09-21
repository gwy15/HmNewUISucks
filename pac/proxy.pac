function FindProxyForURL(url, host) {
    var proxy = "PROXY 192.168.137.1:8080";

    if (shExpMatch(host, "*.jr.moefantasy.com")) return proxy;

    return "DIRECT";
}
