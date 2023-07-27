# Terraform CDK | Cloudflare

This repository contains an example of using Terraform to manage Cloudflare resources. With this Terraform configuration, you can automate the provisioning and management of your Cloudflare settings.

<details>
  <summary>Features</summary>
    
- Azure Backend :x:
- S3 Backend ✅
- Cloudflare Zone ✅
- Cloudflare Record ✅
- Pytest :x: 
</details>

###  Prerequisites
Before you begin, make sure you have the following installed:

- [Terraform CDK](https://developer.hashicorp.com/terraform/cdktf) 
- Cloudflare API Token - You will need an API token with permissions to manage Cloudflare resources.
- Pipenv
- Python

### Getting Started
To get started, follow these steps:

1. Clone this repository to your local machine:
```bash
git clone https://github.com/l33t-sh/terraform-cdk-cloudflare.git
cd terraform-cdk-cloudflare
```

2. Create a `config.yml`using the example provided in the repository
3. Run:
```bash
pipenv shell
cdktf deploy cloudflare-stack
```

Terraform will now create the specified Cloudflare resources based on the configuration in this repository.
Folder Structure

### Folder structure 
The repository is organized as follows:

```
├── cdk_functions/(Helper libs)
    └──  get_config.py 
├── cloudflare/
    └──  cloudflare.py (Stack definition)
├── config/
    └──  config_example.yml (Example of the config file)
├── main.py (Main entrypoint)
└── main-test.py (WIP)
```

### Contributing
I welcome contributions! If you find any issues or want to add new features to this example, feel free to open a pull request.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments
Special thanks to the Terraform, Terraform CDK and Cloudflare teams for their excellent tools and services.

### Contact
If you have any questions or need further assistance, please feel free to contact me:

Email: nikolas.lucansky@gmail.com

Happy Terraforming! :rocket:
