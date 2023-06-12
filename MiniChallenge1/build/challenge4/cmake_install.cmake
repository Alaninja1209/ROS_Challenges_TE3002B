# Install script for directory: /home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/src/challenge4

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/build/challenge4/catkin_generated/installspace/challenge4.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/challenge4/cmake" TYPE FILE FILES
    "/home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/build/challenge4/catkin_generated/installspace/challenge4Config.cmake"
    "/home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/build/challenge4/catkin_generated/installspace/challenge4Config-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/challenge4" TYPE FILE FILES "/home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/src/challenge4/package.xml")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/challenge4" TYPE PROGRAM FILES "/home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/build/challenge4/catkin_generated/installspace/lane_detector.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/challenge4" TYPE PROGRAM FILES "/home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/build/challenge4/catkin_generated/installspace/follow_it.py")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/challenge4" TYPE PROGRAM FILES "/home/alfredo1209/Documentos/RoboticaInteligente/Manchester/MiniChallenge1/build/challenge4/catkin_generated/installspace/photo_cap.py")
endif()

