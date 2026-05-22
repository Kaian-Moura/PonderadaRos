from setuptools import setup

package_name = 'dog_draw_pkg'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Manus',
    maintainer_email='manus@example.com',
    description='Pacote ROS 2 para desenhar um cachorro no Turtlesim',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'draw_node = dog_draw_pkg.draw_node:main',
        ],
    },
)
