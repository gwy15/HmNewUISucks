function FindProxyForURL(url, host) {
    var proxy = "PROXY gwy15.tk:8999";

    if (shExpMatch(host, "*.jr.moefantasy.com")) return proxy;

    return "DIRECT";
}
