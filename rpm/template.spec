%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-cv-bridge
Version:        3.4.0
Release:        2%{?dist}%{?release_suffix}
Summary:        ROS cv_bridge package

License:        Apache License 2.0 and BSD
URL:            http://www.ros.org/wiki/cv_bridge
Source0:        %{name}-%{version}.tar.gz

Requires:       boost-python3
Requires:       opencv-devel
Requires:       python3-numpy
Requires:       python3-opencv
Requires:       ros-rolling-ament-index-python
Requires:       ros-rolling-rclcpp
Requires:       ros-rolling-rcpputils
Requires:       ros-rolling-sensor-msgs
Requires:       ros-rolling-ros-workspace
BuildRequires:  boost-devel
BuildRequires:  opencv-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-opencv
BuildRequires:  ros-rolling-ament-cmake-ros
BuildRequires:  ros-rolling-python-cmake-module
BuildRequires:  ros-rolling-rclcpp
BuildRequires:  ros-rolling-rcpputils
BuildRequires:  ros-rolling-sensor-msgs
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-cmake-gtest
BuildRequires:  ros-rolling-ament-cmake-pytest
BuildRequires:  ros-rolling-ament-lint-auto
BuildRequires:  ros-rolling-ament-lint-common
%endif

%description
This contains CvBridge, which converts between ROS2 Image messages and OpenCV
images.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Tue Jun 20 2023 Kenji Brameld <kenjibrameld@gmail.com> - 3.4.0-2
- Autogenerated by Bloom

