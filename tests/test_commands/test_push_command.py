import os
from pyfakefs import fake_filesystem_unittest

from devbox.commands.info_display_command import InfoDisplayCommandExecutor
from devbox.commands.push_command import PushCommandExecutor


class TestPushCommand(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_build_package_package_created(self):
        # Arrange
        self.fs.CreateFile('my-app/devbox.yaml', contents="""
tosca_definitions_version: tosca_simple_yaml_1_0

topology_template:
  node_templates:
    python_server1:
      type: tosca.nodes.Python
      properties:
        ports_bindings:
          type: string
          default: "{1234:80}"
      artifacts:
        binaries:
          file: binaries.zip
          deploy_path: mybin
    python_client1:
      type: tosca.nodes.Python

node_types:
  tosca.nodes.Python:
    derived_from: tosca.nodes.SoftwareComponent
    properties:
      deployment_image:
        type: string
        default: rastasheep/ubuntu-sshd
      deployment_command:
        type: string
        default: /bin/sh
      deployment_ports:
        type: list
        default: [22, 1234]
      ports_bindings:
        type: string
        required: false
      provisioning_instruction:
        type: string
        default: playbook.yaml
""")

        self.fs.CreateFile('my-app/playbook.yaml', contents="""
---
- hosts: all
  remote_user: root
  tasks:
""")
        self.fs.CreateFile('my-app/binaries.zip', contents='CONTENT')

        os.chdir('my-app')

        command_executor = PushCommandExecutor()

        # Act
        command_executor.push('devbox.yaml', 'docker', 'ansible')

        InfoDisplayCommandExecutor().display_info('devbox.yaml', 'docker')
