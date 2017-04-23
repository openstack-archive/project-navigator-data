Project Navigator Data
======================

Each release should contain a file for each Official OpenStack service that
should contain an extraction from the default version discovery document for
that service for that release. The file can be maintained by hand, but the
following describes how to derive the contents for each service from a running
copy of the service.

Each file shold be named after the service name, e.g. "cinder".

The structure of each file is the same as in the `API WG document`_ on version
discovery, minus the links section, which obviously does not make sense for
the project navigator.

Each service dictionary should contain a top level dictionary with a key
`versions` that contains a list of dictionaries that have the following keys:

 * status, required: can be one of CURRENT, SUPPORTED, DEPRECATED, EXPERIMENTAL
 * id, required: the major api version, in the form vX.X
 * max_version, optional: the maximum microversion supported, in the form X.XX
 * version, optional: same as max_version
 * min_version, optional: the minimum microversion supported, in the form X.XX

If either min_version or max_version are given, they both must be given. If
the service does not have microversions, they should be omitted.

This is also expressed in jsonschema form in the file `schema.json` in this
repository.

.. _API WG document: https://specs.openstack.org/openstack/api-wg/guidelines/microversion_specification.html#version-discovery

Process Description
-------------------

`object-store` doesn't have version discovery document, so it must just be hard
coded.

For the rest of the services, fetch the version discovery document via "GET /"
on the service.

If the service is `compute`, `image`, `network` or `share`, the list of
versions is found in a top level dictionary named 'versions'.

If the service is `identity`, `container_infra` or `key_manager`, the list of
versions is in the 'values' key under the 'versions' key.

For each version in the list of versions, grab status and id, and then
grab max_version and min_version if they exist. If max_version does not exist
but version does, grab version.

`status` values should be uppercased.

If service is `identity` and `status` is "stable", change it to "CURRENT".

If reading pseudo python is easier. This assumes a list called `service_types`,
a requests Session called `client`, a dict of service endpoints called
`endpoints` and a dict that is a mapping of service names keyed by
`service_type` called `service_names`.

.. code-block:: python

  services = {'object-store': {'status': 'CURRENT', 'id': 'v1.0'}}
  for service in services_types:
      doc = client.get(endpoints[service_type]).json()
      if service_type in ('compute', 'network', 'key_manager', 'share'):
          doc = doc['versions']
      elif service_type in ('identity', 'key-manager', 'container-infra'):
          doc = doc['versions']['values']
      versions = []
      for v in doc:
          version = dict(
              status=v['status'],
              id=v['id'])
          max_version=v.get('max_version', v.get('version', None))
          if max_version:
              version['max_version'] = max_version
          min_version=v.get('min_version', None)
          if min_version:
              version['min_version'] = min_version
          versions.append(version)
      service_name = service_name=service_names[service_type]
      json.dump(
          dict(versions=versions),
          open('{service_name}.json'.format(service_name=service_name), 'w'),
          indent=2)

In-repo Maintenance
===================

If each projects wants to maintain a document with the list of versions for a
given release, then updating the version file is a simple matter of a script
to run over the branches of the repos to produce the data.
