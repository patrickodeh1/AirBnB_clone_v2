# Define necessary directories
file { 'versions':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Ensure web_static directory exists
file { 'web_static':
  ensure => 'directory',
  owner  => 'ubuntu',
  group  => 'ubuntu',
  mode   => '0755',
}

# Create a shell script to pack web_static into a .tgz archive
file { '/usr/local/bin/do_pack.sh':
  ensure  => 'file',
  owner   => 'ubuntu',
  group   => 'ubuntu',
  mode    => '0755',
  content => @("EOF")
#!/bin/bash

# Create versions directory if it doesn't exist
if [ ! -d "versions" ]; then
  mkdir versions
fi

# Create a timestamp
timestamp=$(date +'%Y%m%d%H%M%S')

# Create the archive name
archive_name="versions/web_static_${timestamp}.tgz"

# Print the packing message
echo "Packing web_static to ${archive_name}"

# Create the archive
tar -cvzf ${archive_name} web_static

if [ $? -eq 0 ]; then
  echo "Archive created successfully at ${archive_name}"
else
  echo "An error occurred during archive creation"
fi
  | EOF
}

# Execute the script to create the archive
exec { 'pack_web_static':
  command     => '/usr/local/bin/do_pack.sh',
  path        => '/usr/local/bin:/usr/bin:/bin',
  refreshonly => true,
  subscribe   => File['/usr/local/bin/do_pack.sh'],
}
