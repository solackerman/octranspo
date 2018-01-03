from setuptools import setup

setup(
    name='oc_transpo',
    version='0.1.0',
    description='Playing with OC Transpo APIs and Google Cloud',
    long_description='',
    author='Sol Ackermamn',
    author_email='sol.ackerman@gmail.com',
    url='https://github.com/solackerman/octranspo',
    packages=['octranspo'],
    include_package_data=True,
    install_requires=[
    ],
    license="MIT",
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
)
