// **********************************************************************
//
// Copyright (c) 2003-2004 ZeroC, Inc. All rights reserved.
//
// This copy of Ice is licensed to you under the terms described in the
// ICE_LICENSE file included in this distribution.
//
// **********************************************************************

#include <Ice/RoutingTable.h>
#include <Glacier2/RouterI.h>

using namespace std;
using namespace Ice;
using namespace Glacier2;

Glacier2::RouterI::RouterI(const ObjectAdapterPtr& clientAdapter, const ObjectAdapterPtr& serverAdapter,
			   const ConnectionPtr& connection, const string& userId) :
    _communicator(clientAdapter->getCommunicator()),
    _routingTable(new IceInternal::RoutingTable),
    _routingTableTraceLevel(_communicator->getProperties()->getPropertyAsInt("Glacier2.Trace.RoutingTable")),
    _clientProxy(clientAdapter->createProxy(stringToIdentity("dummy"))),
    _clientBlobject(new ClientBlobject(_communicator, _routingTable, "")),
    _connection(connection),
    _userId(userId),
    _timestamp(IceUtil::Time::now()),
    _destroy(false)
{
    if(serverAdapter)
    {
	ObjectPrx& serverProxy = const_cast<ObjectPrx&>(_serverProxy);
	Identity ident;
	ident.name = "dummy";
	ident.category.resize(20);
	for(string::iterator p = ident.category.begin(); p != ident.category.end(); ++p)
	{
	    *p = static_cast<char>(33 + rand() % (127-33)); // We use ASCII 33-126 (from ! to ~, w/o space).
	}
	serverProxy = serverAdapter->createProxy(ident);
	
	ServerBlobjectPtr& serverBlobject = const_cast<ServerBlobjectPtr&>(_serverBlobject);
	serverBlobject = new ServerBlobject(_communicator, connection);
    }
}

Glacier2::RouterI::~RouterI()
{
    assert(_destroy);
}

void
Glacier2::RouterI::destroy()
{
    IceUtil::Mutex::Lock lock(*this);

    assert(!_destroy);

    _clientBlobject->destroy();
    
    if(_serverBlobject)
    {
	_serverBlobject->destroy();
    }

    _destroy = true;
}

ObjectPrx
Glacier2::RouterI::getClientProxy(const Current&) const
{
    // No mutex lock necessary, _clientProxy is immutable and is never destroyed.
    return _clientProxy;
}

ObjectPrx
Glacier2::RouterI::getServerProxy(const Current&) const
{
    // No mutex lock necessary, _serverProxy is immutable and is never destroyed.
    return _serverProxy;
}

void
Glacier2::RouterI::addProxy(const ObjectPrx& proxy, const Current&)
{
    IceUtil::Mutex::Lock lock(*this);

    if(_destroy)
    {
	throw ObjectNotExistException(__FILE__, __LINE__);
    }

    if(_routingTableTraceLevel)
    {
	Trace out(_communicator->getLogger(), "Glacier2");
	out << "adding proxy to routing table:\n" << _communicator->proxyToString(proxy);
    }

    _timestamp = IceUtil::Time::now();

    _routingTable->add(proxy);
}

SessionPrx
Glacier2::RouterI::createSession(const std::string&, const std::string&, const Current&)
{
    assert(false); // Must not be called in this router implementation.
    return 0;
}

void
Glacier2::RouterI::destroySession(const Current&)
{
    assert(false); // Must not be called in this router implementation.
}

ClientBlobjectPtr
Glacier2::RouterI::getClientBlobject() const
{
    IceUtil::Mutex::Lock lock(*this);

    if(_destroy)
    {
	throw ObjectNotExistException(__FILE__, __LINE__);
    }

    _timestamp = IceUtil::Time::now();

    return _clientBlobject;
}

ServerBlobjectPtr
Glacier2::RouterI::getServerBlobject() const
{
    IceUtil::Mutex::Lock lock(*this);

    if(_destroy)
    {
	throw ObjectNotExistException(__FILE__, __LINE__);
    }

    _timestamp = IceUtil::Time::now();

    return _serverBlobject;
}

IceUtil::Time
Glacier2::RouterI::getTimestamp() const
{
    IceUtil::Mutex::TryLock lock(*this);

    if(lock.acquired())
    {
	return _timestamp;
    }
    else
    {
	return IceUtil::Time::now();
    }
}

string
Glacier2::RouterI::toString() const
{
    ostringstream out;

    out << "user-id = " << _userId << '\n';
    if(_serverProxy)
    {
	out << "category = " << _serverProxy->ice_getIdentity().category << '\n';
    }
    out << _connection->toString();

    return out.str();
}
