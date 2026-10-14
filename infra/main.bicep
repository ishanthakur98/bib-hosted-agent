// # DEMO-ONLY: intentional finding - static scanning fixture; DO NOT DEPLOY.
param location string = 'eastus'

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'demoonlystorage'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    // # DEMO-ONLY: intentional finding - unrestricted public network access.
    publicNetworkAccess: 'Enabled'
    // # DEMO-ONLY: intentional finding - permits public blob access.
    allowBlobPublicAccess: true
    // # DEMO-ONLY: intentional finding - permits unencrypted HTTP traffic.
    supportsHttpsTrafficOnly: false
  }
}

resource registry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: 'demoonlyregistry'
  location: location
  sku: {
    name: 'Basic'
  }
  properties: {
    // # DEMO-ONLY: intentional finding - enables registry admin credentials.
    adminUserEnabled: true
  }
}