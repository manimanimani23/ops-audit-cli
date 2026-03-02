from setuptools import setup, find_packages

setup(
    name='ops-audit-cli',
    version='0.1.0',
    packages=find_packages(),
    py_modules=['ops_audit_cli'],
    include_package_data=True,
    install_requires=[
        # 必要な依存関係があればここに記述
        # 'requests',
    ],
    entry_points={
        'console_scripts': [
            'ops-audit = ops_audit_cli:main',
        ],
    },
    author='Mani',
    author_email='mani@openclaw.ai',
    description='A command-line interface for operational auditing.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/openclaw/mani', # 仮のURL。後で更新が必要な場合があります。
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)