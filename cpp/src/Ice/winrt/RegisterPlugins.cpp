// **********************************************************************
//
// Copyright (c) 2003-2015 ZeroC, Inc. All rights reserved.
//
// This copy of Ice Touch is licensed to you under the terms described in the
// ICE_TOUCH_LICENSE file included in this distribution.
//
// **********************************************************************

#include <Ice/Initialize.h>
#include <Ice/RegisterPlugins.h>

using namespace std;
using namespace Ice;
using namespace IceInternal;

extern "C"
{

Plugin* createIceUDP(const CommunicatorPtr&, const string&, const StringSeq&);
Plugin* createIceTCP(const CommunicatorPtr&, const string&, const StringSeq&);
Plugin* createIceSSL(const CommunicatorPtr&, const string&, const StringSeq&);
Plugin* createIceDiscovery(const CommunicatorPtr&, const string&, const StringSeq&);
Plugin* createIceLocatorDiscovery(const CommunicatorPtr&, const string&, const StringSeq&);

}

RegisterPluginsInit::RegisterPluginsInit()
{
    registerPluginFactory("IceUDP", createIceUDP, true);
    registerPluginFactory("IceTCP", createIceTCP, true);
    registerPluginFactory("IceSSL", createIceSSL, true);
    registerPluginFactory("IceDiscovery", createIceDiscovery, false);
    registerPluginFactory("IceLocatorDiscovery", createIceLocatorDiscovery, false);
}
