/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (http://www.swig.org).
 * Version 1.3.36
 * 
 * This file is not intended to be easily readable and contains a number of 
 * coding conventions designed to improve portability and efficiency. Do not make
 * changes to this file unless you know what you are doing--modify the SWIG 
 * interface file instead. 
 * ----------------------------------------------------------------------------- */

#ifndef SWIG_annchienta_WRAP_H_
#define SWIG_annchienta_WRAP_H_

#include <map>
#include <string>


class SwigDirector_Cacheable : public Annchienta::Cacheable, public Swig::Director {

public:
    SwigDirector_Cacheable(PyObject *self, char const *fileName);
    virtual ~SwigDirector_Cacheable();
    virtual Annchienta::CacheableType getCacheableType() const;


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class Cacheable doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[1];
#endif

};


class SwigDirector_Surface : public Annchienta::Surface, public Swig::Director {

public:
    SwigDirector_Surface(PyObject *self, int width, int height, int pixelSize = 3);
    SwigDirector_Surface(PyObject *self, char const *filename);
    virtual ~SwigDirector_Surface();
    virtual Annchienta::CacheableType getCacheableType() const;


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class Surface doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[1];
#endif

};


class SwigDirector_Sound : public Annchienta::Sound, public Swig::Director {

public:
    SwigDirector_Sound(PyObject *self, char const *filename);
    virtual ~SwigDirector_Sound();
    virtual Annchienta::CacheableType getCacheableType() const;


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class Sound doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[1];
#endif

};


class SwigDirector_Entity : public Annchienta::Entity, public Swig::Director {

public:
    SwigDirector_Entity(PyObject *self, char const *name = "none");
    virtual ~SwigDirector_Entity();
    virtual Annchienta::EntityType getEntityType() const;
    virtual void draw();
    virtual void update();
    virtual int getDepth();
    virtual Annchienta::Mask *getMask() const;
    virtual Annchienta::Point getMaskPosition() const;
    virtual bool collidesWith(Annchienta::Entity *other) const;


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class Entity doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[7];
#endif

};


class SwigDirector_Tile : public Annchienta::Tile, public Swig::Director {

public:
    SwigDirector_Tile(PyObject *self, Annchienta::TileSet *arg0, Annchienta::Point arg1, int arg2, Annchienta::Point arg3, int arg4, Annchienta::Point arg5, int arg6, Annchienta::Point arg7, int arg8, int ssOffset = 0, int ss = 0);
    virtual ~SwigDirector_Tile();
    virtual Annchienta::EntityType getEntityType() const;
    virtual void draw();
    virtual void update();
    virtual int getDepth();
    virtual Annchienta::Mask *getMask() const;
    virtual Annchienta::Point getMaskPosition() const;
    virtual bool collidesWith(Annchienta::Entity *other) const;


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class Tile doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[7];
#endif

};


class SwigDirector_Mask : public Annchienta::Mask, public Swig::Director {

public:
    SwigDirector_Mask(PyObject *self, char const *filename);
    SwigDirector_Mask(PyObject *self, int w, int h);
    virtual ~SwigDirector_Mask();
    virtual Annchienta::CacheableType getCacheableType() const;


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class Mask doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[1];
#endif

};


class SwigDirector_StaticObject : public Annchienta::StaticObject, public Swig::Director {

public:
    SwigDirector_StaticObject(PyObject *self, char const *name, char const *configfile);
    SwigDirector_StaticObject(PyObject *self, char const *name, Annchienta::Surface *surf, Annchienta::Mask *mask);
    virtual ~SwigDirector_StaticObject();
    virtual Annchienta::EntityType getEntityType() const;
    virtual void draw();
    virtual void update();
    virtual int getDepth();
    virtual Annchienta::Mask *getMask() const;
    virtual Annchienta::Point getMaskPosition() const;
    virtual bool collidesWith(Annchienta::Entity *other) const;
    virtual void setPosition(Annchienta::Point position);
    virtual Annchienta::Point getPosition() const;
    virtual void setSprite(char const *filename);
    virtual void setPassable(bool passable);
    virtual bool isPassable() const;
    virtual void setOnInteractScript(char const *script);
    virtual void setOnInteractCode(char const *code);
    virtual bool canInteract() const;
    virtual void onInteract();
    virtual void freeze(bool arg0);
    virtual bool stepTo(Annchienta::Point arg0);
    virtual void setStandAnimation(bool b = false);
    virtual void lookAt(Annchienta::StaticObject *other);


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class StaticObject doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[21];
#endif

};


class SwigDirector_Person : public Annchienta::Person, public Swig::Director {

public:
    SwigDirector_Person(PyObject *self, char const *name, char const *configFile);
    virtual ~SwigDirector_Person();
    virtual Annchienta::EntityType getEntityType() const;
    virtual void draw();
    virtual void update();
    virtual int getDepth();
    virtual Annchienta::Mask *getMask() const;
    virtual Annchienta::Point getMaskPosition() const;
    virtual bool collidesWith(Annchienta::Entity *other) const;
    virtual void setPosition(Annchienta::Point position);
    virtual Annchienta::Point getPosition() const;
    virtual void setSprite(char const *filename);
    virtual void setPassable(bool passable);
    virtual bool isPassable() const;
    virtual void setOnInteractScript(char const *script);
    virtual void setOnInteractCode(char const *code);
    virtual bool canInteract() const;
    virtual void onInteract();
    virtual void freeze(bool value);
    virtual void setStandAnimation(bool forceFromHeading = false);
    virtual void lookAt(Annchienta::StaticObject *object);
    virtual void setSpeed(float speed);
    virtual float getSpeed() const;
    virtual bool move(int x, int y, bool force = false);
    virtual bool stepTo(Annchienta::Point point, bool force = true);
    virtual bool isFrozen() const;
    virtual void setControl(Annchienta::PersonControl *personControl);
    virtual void setInputControl();
    virtual void setSampleControl();
    virtual void setNullControl();
    virtual void collisionWithLayerAreas();


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class Person doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[32];
#endif

};


class SwigDirector_PersonControl : public Annchienta::PersonControl, public Swig::Director {

public:
    SwigDirector_PersonControl(PyObject *self, Annchienta::Person *person);
    virtual ~SwigDirector_PersonControl();
    virtual void affect();


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class PersonControl doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[1];
#endif

};


class SwigDirector_SamplePersonControl : public Annchienta::SamplePersonControl, public Swig::Director {

public:
    SwigDirector_SamplePersonControl(PyObject *self, Annchienta::Person *person);
    virtual ~SwigDirector_SamplePersonControl();
    virtual void affect();


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class SamplePersonControl doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[1];
#endif

};


class SwigDirector_InputPersonControl : public Annchienta::InputPersonControl, public Swig::Director {

public:
    SwigDirector_InputPersonControl(PyObject *self, Annchienta::Person *person);
    virtual ~SwigDirector_InputPersonControl();
    virtual void affect();


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class InputPersonControl doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[1];
#endif

};


class SwigDirector_FollowPathPersonControl : public Annchienta::FollowPathPersonControl, public Swig::Director {

public:
    SwigDirector_FollowPathPersonControl(PyObject *self, Annchienta::Person *person);
    virtual ~SwigDirector_FollowPathPersonControl();
    virtual void affect();


/* Internal Director utilities */
public:
    bool swig_get_inner(const char* name) const {
      std::map<std::string, bool>::const_iterator iv = inner.find(name);
      return (iv != inner.end() ? iv->second : false);
    }

    void swig_set_inner(const char* name, bool val) const
    { inner[name] = val;}

private:
    mutable std::map<std::string, bool> inner;


#if defined(SWIG_PYTHON_DIRECTOR_VTABLE)
/* VTable implementation */
    PyObject *swig_get_method(size_t method_index, const char *method_name) const {
      PyObject *method = vtable[method_index];
      if (!method) {
        swig::PyObject_var name = PyString_FromString(method_name);
        method = PyObject_GetAttr(swig_get_self(), name);
        if (method == NULL) {
          std::string msg = "Method in class FollowPathPersonControl doesn't exist, undefined ";
          msg += method_name;
          Swig::DirectorMethodException::raise(msg.c_str());
        }
        vtable[method_index] = method;
      };
      return method;
    }
private:
    mutable swig::PyObject_var vtable[1];
#endif

};


#endif
