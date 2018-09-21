function FindProxyForURL(url, host)
{
    var proxy = "PROXY 192.168.137.1:8080";
    // return proxy;

    // if (shExpMatch(url, "http://version*jr.moefantasy.com/index/checkVer*"))
    if (url.toLowerCase().indexOf("index/checkver") >= 0)
        return proxy;
    else if (url.toLowerCase().indexOf("index/getinitconfigs") >= 0)
        return proxy;
    else if (url.toLowerCase().indexOf("active/getuserdata") >= 0)
        return proxy;
    else
        return "DIRECT";
}
